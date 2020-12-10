from .dicts import LanguageParser
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebParser(object):
    """
    Class to deal with different parsing event
    """
    def __init__(self, **kwargs):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.url = kwargs.get("url", "https://www.avito.ru/")
        self.language_parser = LanguageParser()

    def get_num_of_posts(self, pair: dict):
        """
        Gets number of posts for the pair of region and phrase
        :param pair:
        :return:
        """
        phrase = str(pair["phrase"])  # phrase from the pair
        region = str(pair["region"])  # region from the pair
        self.browser.get(self.url)  # opens avito.ru
        search_field = self.browser.find_element_by_css_selector(
            "input[id='search'][placeholder='Поиск по объявлениям']"
        )  # gets search field
        search_field.click()  # clicks on the search field
        sleep(0.5)  # delay after the click
        search_field.send_keys(phrase)  # fills search field with the phrase
        region_field = self.browser.find_element_by_css_selector(
            "div[data-marker='search-form/region']"
        )  # gets field with the region options
        region_field.click()  # clicks on the region field
        sleep(1)
        region_input = self.browser.find_element_by_css_selector(
            "input[placeholder='Город, регион или Россия']"
        )  # gets region input element
        region_input.click()  # clicks on region input
        region_input.send_keys(region)  # fills the region
        sleep(1)  # delay after the filling
        option_button = self.browser.find_element_by_css_selector(
            "li[data-marker='suggest(0)']"
        )  # first element from the list of options
        option_button.click()
        search_button = self.browser.find_element_by_css_selector(
            "button[data-marker='popup-location/save-button']"
        )  # gets the search button
        search_button.click()  # clicks in the search button

        sleep(2)  # delay until posts are loaded
        try:
            # Tries to get number of posts
            num_of_posts_span = self.browser.find_element_by_css_selector(
                "span[data-marker='page-title/count']"
            )  # element with the number of posts
            num_of_posts = str(num_of_posts_span.get_attribute("innerHTML"))  # gets num of posts
            num_of_posts = num_of_posts.replace("&nbsp;", "")  # deletes spaces from the string
        except Exception:
            #  There are no posts on this topic
            num_of_posts = "0"  # sets number of posts to 0
        return num_of_posts

    def get_top_posts(self):
        """
        Gets links for the top 5 posts on a page
        :return: string with all links separated by ','
        """
        res = ""  # result to return

        #  list of all items links on the page:
        links = list(self.browser.find_elements_by_css_selector("a[data-marker='item-title']"))
        for i in range(5):
            try:
                link = links[i]  # picks a current link
                address = link.get_attribute("href")  # gets url of the post
                res += str(address) + ","  # adds the url to the result
            except Exception:
                # If there are less than 5 posts
                break
        return res[:-1]









