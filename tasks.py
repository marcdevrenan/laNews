from robocorp.tasks import task
from loguru import logger

from src.services.la_news import LANews

@task
def Start():
    try:
        LANews().process()
    except Exception as e:
        logger.error(f"Process execution error: {e}")


if __name__ == "__main__":
    Start()
