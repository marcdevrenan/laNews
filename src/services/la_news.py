from RPA.Browser.Selenium import Selenium
from loguru import logger
from src.config import BASE_URL, SEARCH_PHRASE, NEWS_TOPIC
from src.resources.locators import Locator as LO
from src.utils.toolbox import Toolbox
from src.services.crawler import Crawler

import time


class LANews:
    def __init__(self) -> None:
        self.browser = Selenium()
        self.process()
    
    def open_website(self):
        logger.info(f'Opening {BASE_URL}')
        self.browser.open_available_browser(BASE_URL)
        self.browser.maximize_browser_window()
        
    def search_news(self):
        logger.info(f'Searching for {SEARCH_PHRASE}')
        self.browser.click_button_when_visible(LO.SEARCH_BUTTON)
        self.browser.input_text_when_element_is_visible(LO.SEARCH_FIELD, SEARCH_PHRASE)
        self.browser.press_keys(LO.SEARCH_FIELD, 'ENTER')
    
    def filter_topic(self):
        logger.info(f'Filtering topic {NEWS_TOPIC}')
        self.browser.click_button_when_visible(LO.SHOW_TOPICS)
        self.browser.click_button_when_visible(f'//label[contains(span, "{NEWS_TOPIC}")]/input[@type="checkbox"]')
            
    def sort_newest(self):
        logger.info('Sorting by most recent news')
        self.browser.wait_until_element_is_visible(LO.SORT_BY, 2000)
        self.browser.click_element_when_visible(LO.SORT_BY)
        self.browser.wait_until_element_is_visible(LO.SORT_BY_NEWEST, 2000)
        self.browser.click_element_when_visible(LO.SORT_BY_NEWEST)
    
    def process(self):
        try:
            self.open_website()
            self.search_news()
            self.filter_topic()
            time.sleep(2)
            self.sort_newest()
            time.sleep(2)
            articles = Crawler.extract_news(self)
            Toolbox.excel_generator(articles)
        except Exception as e:
            logger.error(f'Error during step execution: {e}')
            return None
        