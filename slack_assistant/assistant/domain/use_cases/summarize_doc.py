from typing import List
from infrastructure.SlackClient import SlackClient
from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
from .prompt_sum_doc import prompt
import re
class Summarize_doc:
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

    def summarize_doc1(self, links_list, texts_list) -> str:
        """
        Summarize the input text based on predefined rules.

        Args:
            input_text (str): The text to be summarized.

        Returns:
            str: The summarized text.
        """
        formatted_template = self.prompt.format(links_input = links_list, texts_input = texts_list)
        response = self.bot.invoke(formatted_template)
        return response.text
    
    def get_links_and_texts(self,slack_bot_token, channel_id, thread_id):
        bot = SlackClient(slack_bot_token)
        data = bot.get_thread(channel_id, thread_id)
        messages = data.messages
        texts = [message.text for message in messages]
        links = []
        texts = []
        for msg in messages:
            if msg.attachment is not None:
                for att in msg.attachment:
                    links.append(att['url_private'])
                    texts.append(msg.text)
        return links, texts
    
    def summarize_doc(self, slack_bot_token, channel_id, thread_id):
        links_list, texts_list = self.get_links_and_texts(slack_bot_token, channel_id, thread_id)
        result = self.summarize_doc1(links_list,texts_list)
        return result