from typing import List
from infrastructure.SlackClient import SlackClient
from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
from .prompt_sum import prompt
import re
class Summarize:
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

    def summarize(self, input_text: str) -> str:
        """
        Summarize the input text based on predefined rules.

        Args:
            input_text (str): The text to be summarized.

        Returns:
            str: The summarized text.
        """
        formatted_template = self.prompt.format(human_input=input_text)
        response = self.bot.invoke(formatted_template)
        return response.text

    # def get_all_data(self,slack_token ,channel_id, thread_id):
    #     slack = SlackClient(slack_token)
    #     data = slack.get_thread(channel_id,thread_id)
    #     messages = data.messages
    #     attachments = [msg.attachment for msg in messages if msg.attachment is not None]
    #     messages_without_attachment = [msg for msg in messages if msg.attachment is None]
    #     link_file = ""
    #     if attachments != []:
    #         for i in range(len(attachments)):
    #             link_file += " " + attachments[i][0]['url_private']
    #     else: 
    #         link_file += "This message don't have any attachments"
    #     return link_file, messages_without_attachment
    
    # def fetch_thread_messages(self,slack_token ,channel_id, thread_id ):
    #     """
    #     Fetch all messages in a thread from a Slack channel.

    #     Args:
    #         slack_token (str): Slack API token for authentication.
    #         channel_id (str): The ID of the Slack channel.
    #         thread_id (str): The timestamp of the thread.

    #     Returns:
    #         List[str]: A list of text messages from the thread.
    #     """
        
        
        
    #     return texts
    def get_clear_texts(self, slack_token, channel_id, thread_id):
        bot = SlackClient(slack_token)
        data = bot.get_thread(channel_id, thread_id)
        messages = data.messages
        texts = [message.text for message in messages]
        # print(texts)
        pattern = r'<@.*?>'

        # Lọc và loại bỏ các phần tử khớp với biểu thức chính quy
        clear_text = [msg for msg in texts if isinstance(msg, str) and not re.match(pattern, msg)]
        return(clear_text)
    
    def process_list(self, text_list: List[str], max_tokens: int) -> List[str]:
        """
        Process a list of texts, summarizing those that exceed a specified token limit.

        Args:
            text_list (List[str]): The list of texts to be processed.
            max_tokens (int): The maximum token limit for each text.

        Returns:
            List[str]: A list of processed texts, where long texts are summarized.
        """
        processed_list = []
        max_token_limit = 0.25 * max_tokens

        for text in text_list:
            if self.count_token(text) > max_token_limit:
                summarized_text = self.summarize(text)
                processed_list.append(summarized_text)
            else:
                processed_list.append(text)

        return processed_list

    def join_until_max_tokens(self, text_list: List[str], max_tokens: int) -> str:
        """
        Join texts from a list until a maximum token limit is reached.

        Args:
            text_list (List[str]): The list of texts to be joined.
            max_tokens (int): The maximum token limit for the combined text.

        Returns:
            str: The combined text within the token limit.
        """
        combined_text = ""
        current_tokens = 0

        for text in text_list:
            text_tokens = self.count_token(text)

            if current_tokens + text_tokens > max_tokens:
                break

            if combined_text:
                combined_text += " "
            combined_text += text
            current_tokens += text_tokens

        return combined_text

    def process_list_with_limit_tokens(self, lst: List[str], max_tokens: int) -> str:
        """
        Summarize a list of texts by processing them within a maximum token limit.

        Args:
            lst (List[str]): The list of texts to be processed.
            max_tokens (int): The maximum token limit for the entire summary.

        Returns:
            str: The summarized text within the token limit.
        """
        current_text = ""
        summarized_text = ""

        for text in lst:
            new_text = current_text + " " + text
            token_count = self.count_token(new_text)

            if token_count > max_tokens:
                summarized_text += self.summarize(current_text) + " "
                current_text = text  
            else:
                current_text = new_text  

        # Summarize the last piece of text if any
        if current_text:
            summarized_text += self.summarize(current_text)

        return summarized_text

    def summarize_thread(self, slack_token: str, channel_id: str, thread_id: str, max_tokens: int) -> str:
        """
        Summarize all messages in a Slack thread within a token limit.

        Args:
            slack_token (str): Slack API token for authentication.
            channel_id (str): The ID of the Slack channel.
            thread_id (str): The timestamp of the thread.
            max_tokens (int): The maximum token limit for the summary.

        Returns:
            str: The final summarized text for the thread.
        """
        texts = self.get_clear_texts(slack_token, channel_id, thread_id)
        processed_list = self.process_list(texts, max_tokens)
        final_summary = self.process_list_with_limit_tokens(processed_list, max_tokens)
        return final_summary