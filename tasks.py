from src.services.la_news import LANews
from loguru import logger


def Start():
    try:
        LANews().process()
    except Exception as e:
        logger.error("Error")


if __name__ == "__main__":
    Start()
