from dataclasses import dataclass


@dataclass
class Article:
    """Represents a single article"""
    article_url: str
    title: str
    date_scraped: str


@dataclass
class Source:
    """Represents an author and their blog"""
    author: str
    start_page_url: str
    articles: list[Article]
