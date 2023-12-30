import json
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

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
    def __init__(self, blog_name, debug=False):
        self.blog_name = blog_name
        self.debug = debug
        if self.debug:
            self.vault_path = config.DEBUG_VAULT_PATH
        else:
            self.vault_path = config.VAULT_PATH
        self.database_path = config.DB_PATH
        self.debug_n_articles = 1
        self.database = None
        self.link_list = None

    def read_database(self):
        """
        Reads json file to in-memory database
        """
        with open(self.database_path, 'r', encoding="utf-8") as f:
            self.database = json.load(f)
        logging.info("Loaded scraped data file")

    def write_database(self):
        """
        Writes in-memory database to json file
        """
        with open(self.database_path, 'w', encoding="utf-8") as f:
            json.dump(self.database, f)
        logging.info("Wrote scraped data file")

    def get_blog_pages(self):
        """
        Retrieve the list of pages from the blog's start page
        Must be implemented by child class

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Base class BaseBot does not implement.")

    def scrape_pages(self):
        """
        Scrapes pages not found in database for a given blog source
        """
        if self.debug:
            count = 0
        for page in self.link_list:
            if page not in self.database.keys():
                self.scrape_page(page)
                self.update_scraped_status(page)
                logging.info("Scraped page: %s", page)
                if self.debug:
                    count += 1
                    if count >= self.debug_n_articles:
                        return

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

    def update_scraped_status(self, page_url: str) -> None:
        """
        Update the in-memory database with the scraped status

        Args:
            page_url (str): _description_
        """
        now = datetime.now()
        self.database[page_url] = now.isoformat()

    def run(self):
        """
        Run the scraping program
        """
        logging.basicConfig(
            handlers=[
                RotatingFileHandler('logs/logs.log',
                                    maxBytes=100000,
                                    backupCount=10)],
            format='%(asctime)s %(levelname)s %(message)s',
            encoding='utf-8',
            level=logging.INFO
        )
        if self.debug:
            self.database = {}
        else:
            self.read_database()
        self.get_blog_pages()
        self.scrape_pages()
        if not self.debug:
            self.write_database()
