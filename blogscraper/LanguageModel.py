import os
from openai import OpenAI
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

import blogscraper.config as config

# openai.api_key  = os.environ['OPENAI_API_KEY']
client = OpenAI()

class LanguageModel():
    """
    Represents a language model that can be used for many purposes
    Initial use case is to clean up text from scraped blog
    """
    def __init__(self, model:str="mistral"):
        self.model = model
        # self.url = config

    def generate(self, query:str):
        if self.model in ["llama2", "mistral"]:
            return self.generate_local(query=query, model=self.model)
        elif self.model in ["gpt-3.5-turbo", "gpt-3.5-turbo-1106"]:
            return self.generate_gpt(query=query, model=self.model)
        else:
            raise ValueError(f"Invalid model: only valid values are {config.VALID_MODELS}")

    def generate_local(self, query:str, model:str) -> str:
        if model not in ["llama2", "mistral"]:
            raise ValueError("Model must be one of 'llama2', 'mistral'")
        body = {
            "model": model,
            "prompt": query,
            "stream": False
        }
        response = requests.post(config.LOCAL_LLM_URL, json=body)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            logging.error("Error: Failed to generate response.")
            return None

    def generate_gpt(self, query, model="gpt-3.5-turbo", temperature=0):    
        messages = [
        # {'role':'system', 
        #  'content': config.OPENAI_SYSTEM_MESSAGE},    
        {'role':'user',
         'content': query},  
        ] 

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
            # max_tokens=max_tokens
        )

        content = completion.choices[0].message
        usage = dict(completion).get('usage')

        return content, usage


    def get_model(self):
        pass

    def set_model(self, model:str):
        pass

