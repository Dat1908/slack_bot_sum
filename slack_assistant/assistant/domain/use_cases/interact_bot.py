from typing import List
from infrastructure.SlackClient import SlackClient
from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
from .prompt_interact import prompt
import re
class interact:
    def __init__(self, model_name: str, api_key: str):
        """
        Initialize the SlackSummarizer with a GeminiAdapter instance and prompt template.

        Args:
            model_name (str): The name of the LLM model to be used.
            api_key (str): API key for accessing the LLM model.
        """
        self.bot = GeminiAdapter(api_key, model_name)
        self.prompt = prompt

    def count_token(self, text: str) -> int:
        """
        Count the total number of tokens in the given text using the GeminiAdapter model.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            int: The total number of tokens in the text.
        """
        result = self.bot.model.count_tokens(text)
        return result.total_tokens

    def interact_with_human(self, documents, human_input):
        formatted_template = self.prompt.format(documents = documents, human_input = human_input)
        response = self.bot.invoke(formatted_template)
        return response.text