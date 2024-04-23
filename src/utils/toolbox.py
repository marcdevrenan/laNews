import re
from dataclasses import asdict

import pandas
from loguru import logger

from src.config import SEARCH_PHRASE
from src.models.articles import Article


class Toolbox:
    @staticmethod
    def convert_to_filename(text, max_lenght=25, extension=".jpg"):
        cleaned_text = re.sub(r"[^\w\s]", "", text).replace(" ", "_")
        filename = cleaned_text[:max_lenght].strip()
        if len(filename) == max_lenght and filename[max_lenght - 1] == "_":
            filename = filename[: max_lenght - 1].strip().lower()

        return filename + extension

    @staticmethod
    def search_phrase_count(search_phrase, title, description):
        title_count = title.count(search_phrase)
        description_count = description.count(search_phrase)

        return title_count + description_count

    @staticmethod
    def article_has_money_tag(title, description):
        logger.info("Searching for money tag in article")
        template = r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)|\b(\d+)\s*(?:dollars|USD)\b"
        research = re.search(template, title) or re.search(template, description)

        return research is not None

    @staticmethod
    def excel_generator(articles: list[Article]):
        try:
            logger.info("Generating csv file")
            data = pandas.DataFrame([asdict(article) for article in articles])
            data.to_csv(f"temp/results_for_{SEARCH_PHRASE}.csv", index=False)
            logger.info("Results successfully stored")
        except Exception as e:
            logger.error(f"Error generating csv file: {e}")
