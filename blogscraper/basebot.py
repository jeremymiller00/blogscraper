import json
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

from markdownify import markdownify as md
import requests
from bs4 import BeautifulSoup

import blogscraper.config as config


class BaseBot():
    """
    Base class for a bot to scrape the content from a blog
    Each blog type (ie Substack) will need its own subclass
    Custom blogs will need their own custom subclass
    """
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.vault_path = config.VAULT_PATH
        self.scraped_db = config.SCRAPED_DB
        self.link_list = None
        self.scraped = None

    def read_database(self):
        """
        Reads json file to in-memory database
        """
        with open(self.scraped_db, 'r', encoding="utf-8") as f:
            self.scraped = json.load(f)
        logging.info("Loaded scraped data file")

    def write_database(self):
        """
        Writes in-memory database to json file
        """
        with open(self.scraped_db, 'w', encoding="utf-8") as f:
            json.dump(self.scraped, f)
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
        Scrapes pages not found in database for a given blog
        """
        for page in self.link_list and page not in self.scraped.keys():
            self.scrape_page(page)
            self.update_scraped_status(page)
            logging.info("Scraped page: %s", page)

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
        Update the in-memory database with the scraped status

        Args:
            page_url (str): _description_
        """
        # Code to 
        now=datetime.now()
        self.scraped[page_url] = now.isoformat()

    def run(self):
        """
        Run the scraping program
        """
        logging.basicConfig(
            handlers=[RotatingFileHandler('logs/logs.log', maxBytes=100000, backupCount=10)],
            format='%(asctime)s %(levelname)s %(message)s',
            encoding='utf-8', 
            level=logging.INFO
        )
        self.read_database()
        self.get_blog_pages()
        self.scrape_pages()
        self.write_database()
