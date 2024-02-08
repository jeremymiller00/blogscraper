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

    Model strings:
    gpt-3.5-turbo-1106
    gpt-3.5-turbo-0125
    gpt-4-0125-preview
    """
    def __init__(self, model: str = "gpt-3.5-turbo-0125"):
        self.model = model

    def clean_blog(self, text: str) -> (str, list):
        """
        Clean a given scraped text (blog post)
        Possibly in chunks

        Args:
            text (str): text to be cleaned

        Returns:
            str: cleaned text
            list(Usage): list of usage objects
        """
        result = ""
        usages = []
        for t in self.__chunk_text(text):
            prompt = f"""
                You are a text cleaning agent. \
                You receive text delimited by triple dashes \
                which has been scraped from a website which contains a blog post. \
                The text will inevitably be dirty. \
                You have two jobs. \
                Your first job is to return a brief summary at the top, \
                of no more that 100 words \
                under the heading 'Summary:' \
                Your second job is to follow the summary \
                with a cleaned version of the text \
                which contains only the content of the article \
                and is presented under the heading 'Article:'. \
                Remove any metadata or artifacts of scaping the blog website.\
                Return the article in it's entirety. \

                ---{t}---
            """
            content, usage = self.generate(prompt)
            # result += content.get("response")  # ollama format
            result += content.content  # openai format
            usages.append(usage)

        return result, usages

    def generate(self, query: str):
        """
        Generate response from language model
        Consistent abstraction layer

        Args:
            query (str): input to language model

        Raises:
            ValueError: _description_

        Returns:
            __call__: function call to specific language model
        """
        if self.model in ["llama2", "mistral"]:
            return self.__generate_local(query=query, model=self.model)
        elif self.model in ["gpt-3.5-turbo", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0125", "gpt-4-0125-preview"]:
            return self.__generate_gpt(query=query, model=self.model)
        else:
            raise ValueError(f"Invalid model: \
                             only valid values are {config.VALID_MODELS}")

    def __generate_local(self, query: str, model: str) -> str:
        """
        Generate response from language model
        Should only be called by generate()

        Args:
            query (str): input to language model
            model (str): model name

        Raises:
            ValueError: if invalid model name specified

        Returns:
            str: json from local model as dict
            NEEDS FURTHER DEVELOPMENT TO BE FUNCTIONAL
        """
        if model not in ["llama2", "mistral"]:
            raise ValueError("Model must be one of 'llama2', 'mistral'")
        body = {
            "model": model,
            "prompt": query,
            "stream": False
        }
        response = requests.post(config.LOCAL_LLM_URL, json=body, timeout=500)
        if response.status_code == 200:
            # None is needed to match output format with gpt
            return json.loads(response.content), None
        else:
            logging.error("Error: Failed to generate response.")
            return None

    def __generate_gpt(self,
                       query: str,
                       model: str = "gpt-3.5-turbo",
                       temperature: int = 0):
        """
        Generate a response from GPT (3.5)
        Should only be called by generate()

        Args:
            query (str): input to language model
            model (str, optional): Model name. Defaults to "gpt-3.5-turbo".
            temperature (int, optional): model 'creativity'. Defaults to 0.

        Returns:
            str, list(Usage): model response, list of usages (CURRENTLY UNUSED)
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

    def __chunk_text(self, text: str, window: int = 6000) -> list:
        """
        Break text into chunks to prepare for language model

        Args:
            text (str): text to be chunked
            window (int, optional): tokens per chunk. Defaults to 6000.

        Returns:
            list[str]: chunked text
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
    
    # def get_model(self):
    #     """_summary_

    #     Returns:
    #         _type_: _description_
    #     """
    #     return self.model

    # def set_model(self, model: str):
    #     error_string = """
    #     Invalid model name specified.\
    #     The only valid model names are %s"""
    #     if model in config.VALID_MODELS:
    #         self.model = model
    #     else:
    #         raise ValueError(error_string, str(config.VALID_MODELS))
