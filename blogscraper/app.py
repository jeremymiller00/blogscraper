""" 
Main app to run the bots, and get new articles
"""

import sys
import json
import argparse
import logging
from logging.handlers import RotatingFileHandler

from pyfiglet import Figlet

import config
from substack_bot import SubstackBot


class UserInterface():
    def __init__(self) -> None:
        self.database_path = config.DB_PATH
        self.database = None
        self.args = None
        self.parser = None

        logging.basicConfig(
            handlers=[
                RotatingFileHandler('logs/logs.log',
                                    maxBytes=100000,
                                    backupCount=10)],
            format='%(asctime)s %(levelname)s %(message)s',
            encoding='utf-8',
            level=logging.INFO
        )

    def read_database(self):
        """
        Reads json file to in-memory database
        """
        with open(self.database_path, 'r', encoding="utf-8") as f:
            self.database = json.load(f)
        logging.info("Loaded database from file")

    def write_database(self):
        """
        Writes in-memory database to json file
        """
        with open(self.database_path, 'w', encoding="utf-8") as f:
            json.dump(self.database, f)
        logging.info("Wrote database to file")

    def get_sources(self):
        for source, context in config.BLOGS.items():
            print(f"Source: {source}")
            print(f"Context: {context}\n")

    def add_source(self):
        bot = input("Bot: ")
        if bot not in config.VALID_BOTS:
            print(f"Invalid bot. Only valid bots are {config.VALID_BOTS}")
            return
        author = input("Author name: ")
        base_url = input("Base url: ")
        # NEEDS COMPLETION

    def update_source(self):
        pass

    def remove_source(self):
        pass

    def get_new_articles(self):
        for writer, context in config.BLOGS.items():
            if context.get("bot").lower() == "substackbot":
                bot = SubstackBot(blog_name=writer,
                                  database=self.database,
                                  debug=self.args.debug)
                scraped = bot.run()
                self.database.update(scraped)

    def get_articles_for_source(self):
        pass

    def get_args(self):
        parser = argparse.ArgumentParser(
            prog='Blog Scraper',
            description='Auto-get new articles for followed authors.',
            epilog=config.UI_HELP_STRING)
        parser.add_argument('-d', '--debug',
                            action='store_true',
                            help="run in debug mode")
        parser.add_argument('command', choices=["sources", "scrape"])
        args = parser.parse_args()
        self.parser = parser
        self.args = args

    def welcome(self):
        f = Figlet(font='slant')
        print(f.renderText('Blog Scraper'))
    
    def command(self):
        if self.args.command == "sources":
            self.get_sources()
        elif self.args.command == "scrape":
            print("Reading database")
            self.read_database()
            print("Scraping new articles...")
            self.get_new_articles()
            print("Writing database")
            self.write_database()


###############################################
if __name__ == '__main__':
    ui = UserInterface()
    ui.welcome()
    ui.get_args()
    if ui.args.debug:
        print("Debug mode engaged.\n")
    ui.command()
    sys.exit(0)
