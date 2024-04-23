from RPA.Browser.Selenium import Selenium, By
from loguru import logger
from src.config import SEARCH_PHRASE
from src.resources.locators import Locator as LO
from src.models.articles import Article
from src.utils.toolbox import Toolbox

import requests


class Crawler:
    def __init__(self, browser: Selenium) -> None:
        self.browser = browser

    def extract_news(self):
        logger.info("Extracting news")
        articles: list[Article] = []
        self.browser.wait_until_element_is_visible(LO.NEWS)
        news = self.browser.get_webelements(LO.NEWS)
        for article in news:
            title = article.find_element(By.CLASS_NAME, LO.ARTICLE_TITLE).text
            description = article.find_element(
                By.CLASS_NAME, LO.ARTICLE_DESCRIPTION
            ).text
            articles.append(
                Article(
                    title=title,
                    date=article.find_element(
                        By.CLASS_NAME, LO.ARTICLE_PUBLISH_DATE
                    ).text,
                    description=description,
                    picture=Crawler.download_picture(article, title),
                    search_phrase_count=Toolbox.search_phrase_count(
                        SEARCH_PHRASE, title, description
                    ),
                    money_tag=Toolbox.article_has_money_tag(title, description),
                )
            )

        return articles

    @staticmethod
    def download_picture(article, title):
        try:
            logger.info("Downloading article picture of" + title)
            picture = article.find_element(
                By.CLASS_NAME, LO.ARTICLE_PICTURE
            ).get_attribute("srcset")
            picture_url = picture.split(".jpg")[0] + ".jpg"
            file_name = Toolbox.convert_to_filename(title)
            with open(f"temp/{file_name}", "wb") as file:
                file.write(requests.get(picture_url).content)

            return file_name
        except:
            logger.info("Image not found")
            return None
