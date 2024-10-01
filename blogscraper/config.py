""" 
Config module for constants and config values

04201978

"""
UI_HELP_STRING = """
Available Commands:
    sources     show all sources
    scrape      scrape new articles
"""

# authors to follow
BLOGS = {
    # "John Cutler": {
    #     "base_url": "https://cutlefish.substack.com/archive",
    #     "bot": "SubstackBot"
    # },
    "Katie Bauer": {
        "base_url": "https://wrongbutuseful.substack.com/archive",
        "bot": "SubstackBot"
    },
    "Simon Willison": {
        "base_url": "https://simonw.substack.com/archive",
        "bot": "SubstackBot"
    },
    "Stay Sassy": {
        "base_url": "https://staysaasy.com",
        "bot": "StaySaasyBot"
    },
    "Eugene Yan": {
        "base_url": "https://eugeneyan.com/writing",
        "bot": "EugeneYanBot"
    },
    "Chip Huyen": {
        "base_url": "https://huyenchip.com/blog",
        "bot": "ChipHuyenBot"
    },
    "Lenny": {
        "base_url": "https://www.lennysnewsletter.com/t/",
        "bot": "LennyBot"
    },
    "SVPG": {
        "base_url": "https://www.svpg.com/articles",
        "bot": "SVPGBot"
    }
}
# "Lilian Weng" : "https://lilianweng.github.io/archives/"
# chip huyen
# lenny's podcast


# local file stuff
VAULT_PATH = "/Users/Jeremy/Data-Science-Vault/DS-Library/Articles/new/"
DEBUG_VAULT_PATH = "/Users/Jeremy/testvault/"
DB_PATH = "/Users/Jeremy/Documents/Data_Science/Projects/blogscraper/blogscraper/database.json"

# llm stuff
# local models use ollama
VALID_MODELS = ["llama2", "mistral", "gpt-3.5-turbo", "gpt-4-0125-preview"]
LOCAL_LLM_URL = "http://localhost:11434/api/generate"
# PROMPT = """
#     You are an assistant for question-answering tasks. \
#     Use the following pieces of retrieved context to answer the question.\
#     If you don't know the answer, just say that you don't know. \
#     Use three sentences maximum and keep the answer concise. \n\
#     Context: {context} \n
#     Question: {question} \n
#     Answer:
# """

# openai stuff
# OPENAI_SYSTEM_MESSAGE = None

# messages = [
# {'role':'system', 
#  'content':"""You are an assistant who responds\
#  in the style of Dr Seuss."""},    
# {'role':'user',
#  'content':"""write me a very short poem \ 
#  about a happy carrot"""},  
# ] 