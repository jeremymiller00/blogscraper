import json
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

# from markdownify import markdownify as md
# import requests
# from bs4 import BeautifulSoup

from blogscraper import config
from .source import Article, Sourceh


class BaseBot():
    """
    Base class for a bot to scrape the content from a blog
    Each blog type (ie Substack) will need its own subclass
    Custom blogs will need their own custom subclass
    """
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.vault_path = config.VAULT_PATH
        self.database_path = config.DB_PATH
        self.link_list = None
        self.database = None

    def read_database_path(self):
        """
        Reads json file to in-memory database_path
        """
        with open(self.database_path, 'r', encoding="utf-8") as f:
            self.database = json.load(f)
        logging.info("Loaded scraped data file")

    def write_database_path(self):
        """
        Writes in-memory database_path to json file
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

    def scrape_pages(self, debug:bool=False, debug_n_articles:int=1):
        """
        Scrapes pages not found in database_path for a given blog
        """
        if debug:
            count = 0
        for page in self.link_list:
            if page not in self.database.keys():
                self.scrape_page(page)
                self.update_scraped_status(page)
                logging.info("Scraped page: %s", page)
                if debug:
                    count += 1
                    if count >= debug_n_articles:
                        return

    def scrape_page(self, page_url:str):
        """
        Scrape content from a given page
        Must be implemented by child class

        Args:
            page_url (_type_): str

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Base class BaseBot does not implement.")

    def update_scraped_status(self, page_url:str) -> None:
        """
        Update the in-memory database_path with the scraped status

        Args:
            page_url (str): _description_
        """
        now=datetime.now()
        self.database[page_url] = now.isoformat()

    def run(self, debug:bool=False, debug_n_articles:int=1):
        """
        Run the scraping program
        """
        logging.basicConfig(
            handlers=[RotatingFileHandler('logs/logs.log', maxBytes=100000, backupCount=10)],
            format='%(asctime)s %(levelname)s %(message)s',
            encoding='utf-8', 
            level=logging.INFO
        )
        self.read_database_path()
        self.get_blog_pages()
        self.scrape_pages(debug=debug, debug_n_articles=debug_n_articles)
        self.write_database_path()
