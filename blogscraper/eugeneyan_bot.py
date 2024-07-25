import logging
import re

import requests
# from markdownify import markdownify as md
from bs4 import BeautifulSoup

import config
from base_bot import BaseBot
from language_model import LanguageModel


class EugeneYanBot(BaseBot):
    """
    StaySaasy child class for a bot to scrape the content from a Substack blog
    """

    def get_blog_pages(self):
        """
        Code to retrieve the list of pages from the blog's start page
        """
        pages = requests.get(
            config.BLOGS.get(self.blog_name).get("base_url"),
            timeout=100)
        soup = BeautifulSoup(pages.content, 'html.parser')
        link_list = [link.get('href') for link in soup.find_all('a')]
        base = config.BLOGS.get('Eugene Yan').get("base_url")
        link_list_filtered = [link for link in link_list if link[:9] == '/writing/' and len(link) > 9]
        link_list_appended = [base[:-8] + link for link in link_list_filtered]
        self.link_list = link_list_appended
        logging.info("Retrieved page list for: %s", self.blog_name)

    def scrape_page(self, page_url: str):
        """
        Scrape content from a given page

        Args:
            page_url (str): url of an individual blog post
        """
        page = requests.get(page_url, timeout=100)
        soup = BeautifulSoup(page.content, 'html.parser')
        logging.info("Retrieved text for: %s", page_url)
        # lm = LanguageModel()
        # cleaned_text, usages = lm.clean_blog(soup.get_text())
        # logging.info("Cleaned text via LLM for: %s", page_url)
        cleaned_title = soup.title.string.replace(":", " ").replace("/", " ")
        with open(self.vault_path + cleaned_title + ".md", "w",
                  encoding="utf-8") as f:
            f.write(soup.get_text())
        logging.info("Wrote text to file for: %s", page_url)

