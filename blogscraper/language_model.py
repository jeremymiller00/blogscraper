# import os
# from bs4 import BeautifulSoup
# from datetime import datetime
# from logging.handlers import RotatingFileHandler

import json
import logging

import requests
import tiktoken
from openai import OpenAI

import config

client = OpenAI()


class LanguageModel():
    """
    Represents a language model that can be used for many purposes
    Initial use case is to clean up text from scraped blog
    """
    def __init__(self, model: str = "gpt-3.5-turbo-1106"):
        self.model = model

    def generate(self, query: str):
        """_summary_

        Args:
            query (str): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if self.model in ["llama2", "mistral"]:
            return self.generate_local(query=query, model=self.model)
        elif self.model in ["gpt-3.5-turbo", "gpt-3.5-turbo-1106"]:
            return self.generate_gpt(query=query, model=self.model)
        else:
            raise ValueError(f"Invalid model: \
                             only valid values are {config.VALID_MODELS}")

    def generate_local(self, query: str, model: str) -> str:
        if model not in ["llama2", "mistral"]:
            raise ValueError("Model must be one of 'llama2', 'mistral'")
        body = {
            "model": model,
            "prompt": query,
            "stream": False
        }
        response = requests.post(config.LOCAL_LLM_URL, json=body, timeout=500)
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            logging.error("Error: Failed to generate response.")
            return None

    def generate_gpt(self, 
                     query: str,
                     model: str = "gpt-3.5-turbo",
                     temperature: int = 0):
        """_summary_

        Args:
            query (str): _description_
            model (str, optional): _description_. Defaults to "gpt-3.5-turbo".
            temperature (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        messages = [
            {'role': 'user',
             'content': query}
        ]
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        content = completion.choices[0].message
        usage = dict(completion).get('usage')
        return content, usage

    def clean_blog(self, text: str) -> (str, list):
        result = ""
        usages = []
        for t in self.prepare_text(text):
            prompt = f"""
            You are a text cleaning agent. \
            You receive text delimited by triple dashes \
            which has been scraped from a website which contains a blog post. \
            The text will inevitably be dirty. \
            Your job is return a cleaned version of the text \
            which contains only the content of the article. \
            Remove any metadata or artifacts of scaping the blog website.\
            Do not summarize the article, but return it in it's entirety. \

            ---{t}---
            """
            content, usage = self.generate(prompt)
            result += content.content
            usages.append(usage)

        return result, usages

    def prepare_text(self, text: str, window: int = 6000) -> list:
        """_summary_

        Args:
            text (str): _description_
            window (int, optional): _description_. Defaults to 6000.

        Returns:
            list: _description_
        """
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")
        tokens = enc.encode(text)
        n_tokens = len(tokens)

        # if short enough, return text as only element of a list
        if n_tokens < window:
            logging.info("Text not chunked")
            return [text]

        chunks = (n_tokens // window) + 1
        size = len(text) // chunks
        result = []
        # get the first chunk
        result.append(text[:size])
        # get middle chunks
        for i in range(1, chunks - 1):
            result.append(text[size*i:size*(i+1)])
        # get last chunk
        result.append(text[size*(chunks-1):])
        logging.info("Text broken into %s chunks", chunks)

        return result

    def get_model(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.model

    def set_model(self, model: str):
        error_string = """
        Invalid model name specified.\
        The only valid model names are %s"""
        if model in config.VALID_MODELS:
            self.model = model
        else:
            raise ValueError(error_string, str(config.VALID_MODELS))
