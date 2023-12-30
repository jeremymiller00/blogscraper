# import json
# from datetime import datetime
import logging
from collections import Counter

import requests
from markdownify import markdownify as md
from bs4 import BeautifulSoup

import config
from base_bot import BaseBot
from language_model import LanguageModel


class SubstackBot(BaseBot):
    """
    Substack child class for a bot to scrape the content from a Substack blog

    Args:
        BaseBot (_type_): _description_
    """

    def get_blog_pages(self):
        """
        Code to retrieve the list of pages from the blog's start page
        In Substack, links to archive posts are the only links listed twice
        This can be a simple way to get them
        """
        pages = requests.get(
            config.BLOGS.get(self.blog_name).get("base_url"),
            timeout=100)
        soup = BeautifulSoup(pages.content, 'html.parser')
        link_list = [link.get('href') for link in soup.find_all('a')]
        c = Counter()
        c.update(link_list)
        # all links to articles are listed exactly twice on the page
        link_list_filtered = [k for k, v in c.items() if v == 2]
        self.link_list = link_list_filtered
        logging.info("Retrieved page list for: %s", self.blog_name)

    def scrape_page(self, page_url: str):
        """
        Scrape content from a given page

        Args:
            page_url (str): url of an individual blog post
        """
        def is_main(tag):
            return tag.attrs.get('id') == 'main'

        page = requests.get(page_url, timeout=100)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = md(str(soup.body.find_all(is_main)))  # added .div
        logging.info("Retrieved text for: %s", page_url)
        lm = LanguageModel()
        cleaned_text, usages = lm.clean_blog(text)
        logging.info("Cleaned text via LLM for: %s", page_url)
        cleaned_title = soup.title.string.replace(":", " ").replace("/", " ")
        with open(self.vault_path + cleaned_title + ".md", "w",
                  encoding="utf-8") as f:
            f.write(cleaned_text)
        logging.info("Wrote text to file for: %s", page_url)

