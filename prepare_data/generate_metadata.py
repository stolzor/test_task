from typing import List
import spacy
import pandas as pd


def noun_phrase(data: List) -> List:
    """
    Accepts a list then take noun phrase
    :param data:
    :return np_list:
    """
    np_list = []
    nlp = spacy.load("en_core_web_sm")

    for text in data:
        doc = nlp(text)
        temp_list = []
        for chunk in doc.noun_chunks:
            temp_list.append(chunk.root.text)
        np_list.append(temp_list)

    return np_list


def metadata() -> pd.DataFrame:
    df = pd.read_csv('first_task.csv', sep=';')
    text = list(df['article_body'])
    title = list(df['title'])

    np_text = noun_phrase(text)
    np_title = noun_phrase(title)

    df['NP_article_body'] = np_text
    df['NP_title'] = np_title

    df.to_csv('first_task_with_metadata.csv', index=False, sep=';')

    return df


if __name__ == "__main__":
    df = metadata()

    print('Complete!!', df.head())
