""" 
Main app to run the bots, and get new articles
"""

import config
from substack_bot import SubstackBot

for writer, context in config.BLOGS.items():
    if context.get("bot").lower() == "substackbot":
        bot = SubstackBot(blog_name=writer, debug=True)
        bot.run()