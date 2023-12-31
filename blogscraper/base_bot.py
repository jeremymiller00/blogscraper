from datetime import datetime
import logging

# import json
# from markdownify import markdownify as md
# import requests
# from bs4 import BeautifulSoup
# from .source import Article, Source

import config


class BaseBot():
    """
    Base class for a bot to scrape the content from a blog
    Each blog type (ie Substack) will need its own subclass
    Custom blogs will need their own custom subclass
    """
    def __init__(self, blog_name, database, debug=False):
        self.blog_name = blog_name
        self.debug = debug
        if self.debug:
            self.vault_path = config.DEBUG_VAULT_PATH
        else:
            self.vault_path = config.VAULT_PATH
        self.database = database
        self.debug_n_articles = 1
        self.link_list = None

    def get_and_scrape_pages(self) -> dict:
        """
        Get the new article urls, and scrape for a given source
        """
        self.get_blog_pages()
        scraped = self.scrape_pages()
        return scraped

    def get_blog_pages(self):
        """
        Retrieve the list of page urls from the blog's start page
        Must be implemented by child class

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Base class BaseBot does not implement.")

    def scrape_pages(self) -> dict:
        """
        Scrapes pages not found in database for a given blog source
        """
        scraped = {}
        if self.debug:
            count = 0
            self.database = {}  # reset to empty database for debugging
        for page in self.link_list:
            if page not in self.database.keys():
                self.scrape_page(page)
                now = datetime.now()
                scraped[page] = now.isoformat()
                logging.info("Scraped page: %s", page)
                if self.debug:
                    count += 1
                    if count >= self.debug_n_articles:
                        return {}  # to avoid adding to database in debug mode
        
        return scraped

    def scrape_page(self, page_url: str):
        """
        Scrape content from a given page
        Must be implemented by child class

        Args:
            page_url (_type_): str

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Base class BaseBot does not implement.")

