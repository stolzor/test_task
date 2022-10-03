from typing import List, Dict
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By


class ParserFields(object):

    def __init__(self, url: str = "https://www.aceee.org/news"):
        """
        If changed style on page, then change url.
        :param url:
        """
        self.driver = webdriver.Chrome()
        self.url = url
        self.session_id = None

    def parse(self) -> List:
        """
        The method contains all necessary method and parsing process is configured.
        :return:
        """
        path_articles = self.get_path(self.url)  # get paths articles
        for path in path_articles:
            self.parse_necessary_fields(path)

        return path_articles

    def parse_necessary_fields(self, path: str) -> Dict:
        """
        Parsing and formatting next fields:
        title, pubdate, datestring, categories, article_body, tags, external_links
        :param path:
        :return:
        """
        formats = '%B %d, %Y'

        fields_param = {
            'title': {'class': 'hero-text', 'tag': 'div', 'type': 'class', 'func': lambda x: x.split('\n')[-2]},
            'pubdate': {'class': 'summary', 'tag': 'div', 'type': 'class',
                        'func': lambda x: datetime.datetime.strptime(x, formats).strftime('%x')},
            # lambda formats from 'September 21, 2022' to '09/21/22'
            'categories': None,
            'article_body': {'class': 'grid-x grid-margin-x', 'tag': 'div', 'type': 'class'},
            'tags': {'class': 'button hollow tag', 'tag': 'a', 'type': 'class'},
            'external_links': {'class': 'small-6 small-offset-2 medium-5 medium-offset-1 cell', 'tag': 'div',
                               'type': 'class'}}
        """
            this is dict contain name CSS classes and tag, which we can parsing (change it if necessary)
            info about the value in dict:
                'class': name class
                'func': complete formats
                'tag': name tag
                'type': class or id
        """

        fields_dict = {'title': None, 'datestring': None, 'categories': None, 'article_body': None, 'tags': [],
                       'external_links': [], 'pubdate': None}
        print(path)
        self.driver.get(path)

        for key, value in fields_param.items():
            if value is None:
                print(key, 'skip')
                continue
            name, tag, types = value['class'], value['tag'], value['type']
            xpath = f"//{tag}[@{types}='{name}']"

            try:
                if key in ['tags', 'external_links']:
                    res = self.driver.find_elements(By.XPATH, xpath)
                    if key == 'external_links':
                        for link in res[0].find_elements(By.TAG_NAME, 'a'):
                            fields_dict[key].append(link.get_attribute('href'))

                        if len(fields_dict['tags']) != 0:
                            fields_dict[key] = fields_dict[key][:len(fields_dict['tags'])]
                            """
                            since tags and various links are in the same block, 
                            therefore we are forced to delete the last values of the list
                            """

                    else:
                        fields_dict[key].extend([i.text for i in res])
                else:
                    res = fields_param[key]['func'](self.driver.find_element(By.XPATH, xpath).text) \
                        if 'func' in fields_param[key].keys() else self.driver.find_element(By.XPATH, xpath).text

                    fields_dict[key] = res

            except Exception as e:
                print(key, e, 'errors')

        self.driver.close()
        print(fields_dict)
        return fields_dict

    def get_path(self, url: str) -> List:
        """
        Get rows with articles paths.
        :param url:
        :return: path_list
        """
        path_list = []
        self.driver.get(url)
        self.session_id = self.driver.session_id

        rows = self.driver.find_elements(By.CLASS_NAME, 'views-row')

        for row in rows:
            path_list.append(row.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        return path_list

    def quit(self):
        self.driver.quit()
