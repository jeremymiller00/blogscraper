import json
import requests
from collections import Counter
from markdownify import markdownify as md
from bs4 import BeautifulSoup
import markdown
from email.mime.text import MIMEText
from datetime import datetime
import logging

from .BaseBot import BaseBot
import blogscraper.config as config

# Example for a specific blog bot
class SubstackBot(BaseBot):

    def get_blog_pages(self):
        # Code to retrieve the list of pages from the blog's start page
        # In substack pages, links to archive posts are the only links listed twice
        # This can be a simple way to get them
        pages = requests.get(config.blogs.get(self.blog_name))
        soup = BeautifulSoup(pages.content, 'html.parser')
        link_list = [link.get('href') for link in soup.find_all('a')]
        c = Counter()
        c.update(link_list)
        link_list_filtered = [k for k, v in c.items() if v == 2]
        self.link_list = link_list_filtered
        logging.info(f"Retreived page list for: {self.blog_name}")

        return

    def scrape_page(self, page_url):
        # Code to scrape content from a given page
        def is_main(tag):
            return tag.attrs.get('id') == 'main'

        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = md(str(soup.body.find_all(is_main))) # added .div
        logging.info(f"Retreived text for: {page_url}")
        cleaned_title = soup.title.string.replace(":", " ").replace("/", " ")
        with open(self.vault_path + cleaned_title + ".md", "w") as f:
            f.write(text)
        logging.info(f"Wrote text to file for: {page_url}")

        return
