import requests
import json
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

import blogscraper.config as config


class BaseBot():
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.vault_path = config.VAULT_PATH
        self.scraped_db = config.SCRAPED_DB
        self.link_list = None
        self.scraped = None

    def read_scraped(self):
        with open(self.scraped_db, 'r') as f:
            self.scraped = json.load(f)
        logging.info("Loaded scraped data file")

    def write_scraped(self):
        with open(self.scraped_db, 'w') as f:
            json.dump(self.scraped, f)
        logging.info("Wrote scraped data file")

    def get_blog_pages(self):
        # Code to retrieve the list of pages from the blog's start page
        pass

    def scrape_page(self, page_url):
        # Code to scrape content from a given page
        pass

    def scrape_pages(self):
        for page in self.link_list:
            if page not in self.scraped.keys():
                self.scrape_page(page)
                self.update_scraped_status(page)
                logging.info(f"Scraped page: {page}")
        return

    def send_email_notification(self):
        # Code to send an email notification
        pass

    def update_scraped_status(self, page_url):
        # Code to update the database with the scraped status
        now=datetime.now()
        self.scraped[page_url] = now.isoformat()
        return

    def send_email(self, message):
        # This would require allowing less secure apps to access my gmail account
        # Probably not worth it

        # port = 465  # For SSL
        # password = input("Type your password and press enter: ")

        # # Create a secure SSL context
        # context = ssl.create_default_context()

        # with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        #     server.login("jeremymiller00@gmail.com", password)
        #     server.sendmail("jeremymiller00@gmail.com", "jeremymiller00@gmail.com", message)
        pass

    def run(self):

        logging.basicConfig(
            handlers=[RotatingFileHandler('logs/logs.log', maxBytes=100000, backupCount=10)],
            format='%(asctime)s %(levelname)s %(message)s',
            encoding='utf-8', 
            level=logging.INFO
        )

        self.read_scraped()
        self.get_blog_pages()
        self.scrape_pages()
        self.write_scraped()
        return


