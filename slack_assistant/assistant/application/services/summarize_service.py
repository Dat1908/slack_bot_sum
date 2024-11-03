from dotenv import load_dotenv
from domain.use_cases.summarize_thread import Summarize
import os

class SlackSummarizer:
    def __init__(self):
        """
        Initialize the SlackSummarizer class by loading environment variables.
        """
        load_dotenv()
        self.key = os.environ.get("GOOGLE_API_KEY")
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        self.model_name = os.environ.get("MODEL_NAME")
        self.summary = Summarize(model_name=self.model_name, api_key=self.key)
        
    def run(self, channel_id:str, thread_id: str, max_tokens:int) -> str:
        """
        Run the summarization process on a Slack thread.

        Args:
            channel_id (str): The ID of the Slack channel.
            thread_id (str): The timestamp of the thread.
            max_tokens (int): The maximum token limit for the summary.

        Returns:
            str: The summarized text for the thread.
        """
        result = self.summary.summarize_thread(slack_token=self.slack_bot_token,
                                               channel_id = channel_id, 
                                               thread_id = thread_id, 
                                               max_tokens = max_tokens)
        return result