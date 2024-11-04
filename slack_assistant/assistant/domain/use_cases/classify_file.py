from typing import List
from infrastructure.SlackClient import SlackClient
from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
from .prompt_arrange import prompt
import re
class classify_file:
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
    
    def classify_files_and_links(self,slack_bot_token , channel_id, thread_id):
        links, texts = self.get_links_and_texts(slack_bot_token, channel_id, thread_id)
        formatted_template = self.prompt.format(human_input = texts)
        response = self.bot.invoke(formatted_template)
        return links , texts,response.text
    
    def links_and_texts_of_doc(self, slack_bot_token, channel_id, thread_id):
        links,texts ,result = self.classify_files_and_links(slack_bot_token, channel_id, thread_id)
        number_result_text = []
        links_doc = []
        texts_doc = []
        for i in result:
            if ((i == '1') or(i == '0')):
                number_result_text.append(i)
        for i in range(len(number_result_text)):
            if (number_result_text[i] == '1'):
                links_doc.append(links[i])
                texts_doc.append(texts[i])
        return texts_doc, links_doc