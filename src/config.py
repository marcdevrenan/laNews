import os

from dotenv import load_dotenv

load_dotenv(".env")
BASE_URL = "https://www.latimes.com/"
SEARCH_PHRASE = os.environ.get("SEARCH_PHRASE")
NEWS_TOPIC = os.environ.get("NEWS_TOPIC")
