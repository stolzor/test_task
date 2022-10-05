from abc import ABC
from typing import List
import datetime
from selenium.webdriver.common.by import By


class FieldExtractor(ABC):
    key: str
    name: str
    tag: str
    type: str

    def get_path(self):
        return f"//{self.tag}[@{self.type}='{self.name}']"

    def format_result(self, result: str) -> str | List:
        return result


class TitleExtractor(FieldExtractor):
    key = 'title'
    name = 'hero-text'
    tag = 'div'
    type = 'class'

    def format_result(self, result: str) -> str:
        return result.split('\n')[-2]


class PubDateExtractor(FieldExtractor):
    key = 'pubdate'
    name = 'summary'
    tag = 'div'
    type = 'class'

    def format_result(self, result: str) -> str:
        formats = '%B %d, %Y'

        return datetime.datetime.strptime(result, formats).strftime('%x')


class ArticleBodyExtractor(FieldExtractor):
    key = 'article_body'
    name = 'grid-x grid-margin-x'
    tag = 'div'
    type = 'class'

    def format_result(self, result: str) -> str:
        return result


class ExternalLinksExtractor(FieldExtractor):
    key = 'external_links'
    name = 'small-6 small-offset-2 medium-5 medium-offset-1 cell'
    tag = 'div'
    type = 'class'

    def format_result(self, result: List) -> List:
        link_list = []
        for elem in result:
            for link in elem.find_elements(By.TAG_NAME, 'a'):
                link_list.append(link.get_attribute('href'))
        return link_list


class TagsExtractor(FieldExtractor):
    key = 'tags'
    name = 'button hollow tag'
    tag = 'a'
    type = 'class'

    def format_result(self, result: List) -> List:
        return [i.text for i in result]


class CategoriesExtractor(FieldExtractor):
    key = 'categories'
    parent_name = 'hero-text'
    child_name = 'button hollow tag'
    tag = 'div'
    type = 'class'

    def get_path(self):
        return f"//{self.tag}[@class='{self.parent_name}']" \
               f"//{self.tag}[@class='{self.child_name}']"

    def format_result(self, result: str) -> str:
        return result
