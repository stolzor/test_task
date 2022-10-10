import pandas as pd
from models.fields_parser import FieldsParser
from models.paths_parser import PathsParser


def form_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=['title', 'article_body', 'tags', 'categories',
                               'external_links', 'pubdate', 'datestring'])

    print('-----START PARSE PAGE----')
    paths = PathsParser()
    paths_articles = paths.parse_urls()
    # paths_articles = [i[:-1] for i in open('urls.txt')]  ## in order not
    # to constantly parse links,
    # you can comment out two lines from above and uncomment this one
    print('-----END PARSE PAGE----')

    print('-----START PARSE ARTICLES----')
    driver = FieldsParser()

    for path in paths_articles:
        try:
            result = driver.parse(path)
            print(path, ' --- parsing complete!')
            df = pd.concat([df, pd.DataFrame([list(result.values())],
                                             columns=list(result.keys()))])
        except:
            print(path, ' --- unsuccessful parsing.')
    print('-----END PARSE ARTICLES----')

    df.to_csv('first_task.csv', index=False, sep=';')
    driver.quit()

    return df


if __name__ == "__main__":
    df = form_df()
    print(df.head())
