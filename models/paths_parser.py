from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class PathsParser:
    def __init__(self):  # if url changed replace it
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        # setting the "eager" parameter so as not to wait for the full download
        options = Options()
        options.add_argument("--headless")
        # setting for hide the browser while running
        self.driver = webdriver.Chrome(desired_capabilities=caps,
                                       options=options)

    def check_existence(self, page: webdriver) -> bool:
        """
        This method input page and checks if the last page
        :param page:
        :return flag:
        """
        flag = True
        xpath = "//strong[text()='No results available']"

        try:
            page.find_element(By.XPATH, xpath)
            flag = False
        except Exception:
            pass

        return flag

    def parse_urls(self) -> List:
        """
        This method parse all available url contains rows with articles
        :return page_list:
        """
        page_list = []
        counter_page = 0
        flag = True

        current_page = 'https://www.aceee.org/news?keys=&field_' \
                       'authors_target_id=&field_related_programs_target_id' \
                       '=&field_related_topics_target_id=&' \
                       'sort_bef_combine=created_DESC&' \
                       'sort_by=created&sort_order=DESC&page={}'

        while flag:
            current_url = current_page.format(counter_page)
            self.driver.get(current_url)
            flag = self.check_existence(self.driver)
            if not flag:
                break
            page_list.extend(self.parse_paths(current_url))
            print(current_url, '--- complete!')

            counter_page += 1
        self.driver.quit()
        return page_list

    def parse_paths(self, url: str) -> List:
        """
        Get rows with articles paths
        :param url:
        :return path_list:
        """
        path_list = []
        self.driver.get(url)

        rows = self.driver.find_elements(By.CLASS_NAME, 'views-row')

        for row in rows:
            path_list.append(
                row.find_element(By.TAG_NAME, 'a').get_attribute('href')
            )

        return path_list
