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
from staysaasy_bot import StaySaasyBot
from eugeneyan_bot import EugeneYanBot
from chiphuyen_bot import ChipHuyenBot
from lenny_bot import LennyBot
from svpg_bot import SVPGBot


class UserInterface():
    def __init__(self, logfile_path: str = 'logs/logs.log') -> None:
        self.database_path = config.DB_PATH
        self.logfile_path = logfile_path
        self.database = None
        self.args = None
        self.parser = None

        logging.basicConfig(
            handlers=[
                RotatingFileHandler(self.logfile_path,
                                    maxBytes=100000,
                                    backupCount=10),
                logging.StreamHandler()],  # send log messages to console
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
        """
        Show list of authors / sources currently defined
        """
        for source, context in config.BLOGS.items():
            print(f"Source: {source}")
            print(f"Context: {context}\n")
        logging.info("Showed sources")

    def add_source(self):
        """ 
        Add a new blog to the roster of those to follow        
        """
        bot = input("Bot: ")
        if bot not in config.VALID_BOTS:
            print(f"Invalid bot. Only valid bots are {config.VALID_BOTS}")
            return
        author = input("Author name: ")
        base_url = input("Base url: ")
        sources = config.BLOGS
        sources.update({author: {"base_url": base_url, "bot": bot}})
        # NEEDS COMPLETION
        logging.info("Added source")

    def update_source(self):
        """ 
        Update an existing entry in the roster of blogs to follow
        """
        pass

    def remove_source(self):
        """ 
        Remove an entry from the roster of blogs to follow
        """
        pass

    def get_new_articles(self):
        """ 
        Get new article for all blogs in the roster
        """
        for writer, context in config.BLOGS.items():
            logging.info("Getting new articles for %s", writer)
            bot = self._create_bot(writer=writer, context=context)
            scraped = bot.get_and_scrape_pages()
            self.database.update(scraped)
            if self.args.debug:  # break out of loop after first writer
                return

    def _create_bot(self, writer, context):
        klass = globals()[context.get("bot")]
        instance = klass(blog_name=writer,
                         database=self.database,
                         debug=self.args.debug)
        
        return instance

    def get_articles_for_source(self):
        """
        Get the articles for only a single source
        """
        pass

    def get_args(self):
        """ 
        Get command line args
        """
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
        logging.info("Args retrieved from console")

    def welcome(self):
        f = Figlet(font='slant')
        print(f.renderText('Blog Scraper'))
    
    def command(self):
        """
        Executes workflow for the given command
        """
        if self.args.command == "sources":
            self.get_sources()
        elif self.args.command == "add":
            self.add_source()
        elif self.args.command == "scrape":
            self.read_database()
            self.get_new_articles()
            if not self.args.debug:
                self.write_database()


###############################################
if __name__ == '__main__':
    ui = UserInterface()
    ui.get_args()
    ui.welcome()
    if ui.args.debug:
        print("Debug mode engaged.\n")
    ui.command()
    sys.exit(0)
