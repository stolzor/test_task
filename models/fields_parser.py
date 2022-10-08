from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from .schemas import TitleExtractor, ArticleBodyExtractor,\
    ExternalLinksExtractor, PubDateExtractor, TagsExtractor,\
    CategoriesExtractor


class FieldsParser(object):

    def __init__(self):
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        # setting the "eager" parameter so as not to wait for the full download
        options = Options()
        options.add_argument("--headless")
        # setting for hide the browser while running
        self.driver = webdriver.Chrome(desired_capabilities=caps,
                                       options=options)

    def parse(self, url: str) -> Dict:
        """
        Parsing and formatting next fields:
        title, pubdate, article_body, tags, external_links, datestring
        :param url:
        :return fields_dict:
        """
        fields_class = [TitleExtractor(), ArticleBodyExtractor(),
                        TagsExtractor(), CategoriesExtractor(),
                        PubDateExtractor(), ExternalLinksExtractor()]

        fields_dict = {'title': '', 'article_body': '', 'tags': [],
                       'categories': '', 'external_links': [], 'pubdate': '',
                       'datestring': '2022-05-10'}
        self.driver.get(url)

        for i in range(len(fields_class)):
            extractor = fields_class[i]
            xpath = extractor.get_path()
            elem = None

            try:
                if extractor.key not in ['external_links', 'tags']:
                    elem = self.driver.find_element(By.XPATH, xpath).text
                else:
                    elem = self.driver.find_elements(By.XPATH, xpath)
                    elem = elem[:len(fields_dict['tags'])] \
                        if len(fields_dict['tags']) != 0 \
                        and extractor.key == 'external_links' else elem
            except Exception as e:
                print(f'{extractor.key} have ERRORS!!', e)

            param = extractor.format_result(elem)
            fields_dict[extractor.key] = param

        return fields_dict

    def quit(self):
        """
        This method goes out of the window
        :return:
        """
        self.driver.quit()
