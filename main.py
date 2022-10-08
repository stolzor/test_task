from typing import Union
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

from parsing import form_df
from prepare_data.aggregate import core
from prepare_data.generate_metadata import metadata


def checker():
    try:
        st.session_state['df']
    except:
        'Starting a long computation...'
        with st.spinner('Wait until the parsing is over...'):
            st.session_state['df'] = form_df()
        st.success(f"Done! To parse {len(st.session_state['df'])} articles complete!")


'Hi!'
' Available parameters: Parsing of data (or enter: parsing);' \
    ' Simple bar plot aggregation (or enter: simple);' \
    ' Creating metadata (or enter: metadata).'

option = st.text_input('Enter parameter:', '').lower()
st.write('The current parameter is', option)


if option == 'parsing of data' or option == 'parsing':
    checker()

    st.dataframe(st.session_state['df'])
if option == 'simple aggregation' or option == 'simple':
    checker()

    df_grouped = core(st.session_state['df'])
    df_grouped.plot(kind='bar', figsize=(30, 30))
    st.pyplot(plt)
elif option == 'Creating metadata' or option == 'metadata':
    checker()

    with st.spinner('Wait until the creating metadata is over...'):
        df_metadata = metadata()
    st.dataframe(df_metadata)
else:
    'Please enter available parameters'



