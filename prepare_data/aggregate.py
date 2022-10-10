import pandas as pd
import matplotlib.pyplot as plt


def creating_dict(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creating new data frame with columns: year_month, counter, categories
    :return new_df:
    """
    pubdate = list(df['pubdate'])
    categories = list(df['categories'])

    # creating dict which contains year_month and counter
    d = {}
    for i in pubdate:
        if i[:-3] not in d.keys():
            d[i[:-3]] = [i]
        else:
            d[i[:-3]].append(i)

    n_l = []
    c = 0
    # creating new table with columns: year_month, counter, categories
    for key, value in d.items():
        n_l.append([key, len(value), categories[c]])
        c += 1

    return pd.DataFrame(n_l, columns=['year_month', 'counter', 'categories'])


def grouped(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enter df and grouping necessary columns
    :param df:
    :return result:
    """
    result = (df.groupby(['year_month', 'categories']).agg(
        ['sum'])).sort_values(by=['year_month'])
    return result


def core(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main process
    :return df_grouped:
    """
    df = creating_dict(df)
    df_grouped = grouped(df)
    df_grouped.plot(kind='bar', figsize=(30, 30))
    plt.savefig('../fig.png')
    return df_grouped


if __name__ == '__main__':
    df = pd.read_csv('../first_task.csv', sep=';')
    df_grouped = core(df)
    print(df)
