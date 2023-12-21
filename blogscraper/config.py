""" 
Config module for constants and config values
"""

# authors to follow
BLOGS = {
    "John Cutler" : "https://cutlefish.substack.com/archive",
    "Katie Bauer" : "https://wrongbutuseful.substack.com/archive",
    "Simon Willison" : "https://simonw.substack.com/archive"
}
# "Eugene Yan" : "https://eugeneyan.com/writing/"
# "Lilian Weng" : "https://lilianweng.github.io/archives/"
# stay sassy
# chip huyen


# local file stuff
VAULT_PATH = "/Users/Jeremy/testvault/"
SCRAPED_DB = "/Users/Jeremy/Documents/Data_Science/Projects/blogscraper/blogscraper/scraped.json"


# llm stuff
# local models use ollama
VALID_MODELS = ["llama2", "mistral", "gpt-3.5-turbo"]
LOCAL_LLM_URL = "http://localhost:11434/api/generate"
PROMPT = """
    You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question.\
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise. \n\
    Context: {context} \n
    Question: {question} \n
    Answer:
"""

# openai stuff
OPENAI_SYSTEM_MESSAGE = None

# messages = [
# {'role':'system', 
#  'content':"""You are an assistant who responds\
#  in the style of Dr Seuss."""},    
# {'role':'user',
#  'content':"""write me a very short poem \ 
#  about a happy carrot"""},  
# ] 