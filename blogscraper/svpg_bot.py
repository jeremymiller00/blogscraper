import logging
import re

import requests
from bs4 import BeautifulSoup

import config
from base_bot import BaseBot
from language_model import LanguageModel


class SVPGBot(BaseBot):
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
        link_list_filtered = [link for link in link_list if isinstance(link, str) and link[21:29] == 'insights']
        
        # for svpgbot, need to recursively get links from this list ^^^
        all_links = []
        for link in link_list_filtered:
            pages = requests.get(link, timeout=100)
            soup = BeautifulSoup(pages.content, 'html.parser')
            link_list = [link.get('href') for link in soup.find_all('a')]
            link_list_filtered = [link for link in link_list if isinstance(link, str) and link[12:16] == "svpg"]
            all_links.extend(link_list_filtered)

        all_links = list(set(all_links))
        
        self.link_list = all_links
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
        # cleaned_text, usages = lm.clean_blog(re.sub(r'(?:\r?\n|\r){2,}', "", soup.get_text()))
        # logging.info("Cleaned text via LLM for: %s", page_url)
        cleaned_title = soup.title.string.replace(":", " ").replace("/", " ")
        with open(self.vault_path + cleaned_title + ".md", "w",
                  encoding="utf-8") as f:
            f.write(soup.get_text())
        logging.info("Wrote text to file for: %s", page_url)

