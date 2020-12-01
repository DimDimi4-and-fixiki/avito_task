import requests
from bs4 import BeautifulSoup
from dicts import LanguageParser
from models import AvitoPair
from selenium import webdriver
from time import sleep


class WebParser(object):
    """
    Class to operate with different parsing activities
    """
    def __init__(self, **kwargs):
        self.url = kwargs.get("url", "https://www.avito.ru/")
        self.soup = None  # Beautiful Soup
        self.language_parser = LanguageParser()
        self.browser = webdriver.Chrome("/home/dimdimi4/Documents/avito_exam/chromedriver")

    def get_num_of_posts(self, pair: dict):
        phrase = str(pair["phrase"])  # phrase from the pair
        region = str(pair["region"])  # region from the pair
        self.browser.get(self.url)
        search_field = self.browser.find_element_by_css_selector(
            "input[id='search'][placeholder='Поиск по объявлениям']"
        )
        search_field.click()
        search_field.send_keys(phrase)  # fills search field with the phrase
        region_field = self.browser.find_element_by_css_selector(
            "div[data-marker='search-form/region']"
        )
        region_field.click()
        region_input = self.browser.find_element_by_css_selector(
            "input[placeholder='Город, регион или Россия']"
        )
        region_input.click()
        region_input.send_keys(region)
        sleep(1)
        option_button = self.browser.find_element_by_css_selector(
            "li[data-marker='suggest(0)']"
        )
        option_button.click()
        search_button = self.browser.find_element_by_css_selector(
            "button[data-marker='popup-location/save-button']"
        )
        search_button.click()
        sleep(1)
        try:
            num_of_posts_span = self.browser.find_element_by_css_selector(
                "span[data-marker='page-title/count']"
            )
            num_of_posts = str(num_of_posts_span.get_attribute("innerHTML"))
            num_of_posts = num_of_posts.replace("&nbsp;", "")  # deletes spaces from the string
        except Exception:
            num_of_posts = "0"
        return num_of_posts




