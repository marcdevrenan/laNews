from dataclasses import dataclass


@dataclass
class Article:
    title: str
    date: str
    description: str
    picture: str|None
    search_phrase_count: int
    money_tag: bool