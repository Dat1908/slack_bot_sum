import os
from dotenv import load_dotenv
from domain.use_cases.Recommend import Recommend


class RecommendService:
    """
    A service class that manages the process of generating recommendations
    based on Slack conversations.

    This class loads environment varible to create necessary components
    and provides a simple interface to generate recommendations.

    Attributes:
        slack_bot_token (str): Token for authenticating with the Slack API.
        llm_token (str): Token for authenticating with the Gemini language
            model.
        recommend_ins (Recommend): An instance of the Recommend class for
            generating recommendations.

    Methods:
        serve: Generates a recommendation based on a specific Slack
            conversation.
    """

    def __init__(self):
        """
        Initializes the RecommendService with necessary tokens and model
            information from environment variables
        """
        load_dotenv()
        self.slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.llm_token = os.getenv("GOOGLE_API_KEY")
        self.recommend_ins = Recommend(slack_bot_token=self.slack_bot_token,
                                       llm_token=self.llm_token)

    def serve(self, user_id: str,
              channel_id: str,
              thread_id: str,
              max_tokens: int) -> str:
        """
        Generates a recommendation based on a specific Slack conversation.

        This method retrieves the conversation, formats it into a prompt,
        and then generates a recommendation using the Gemini language model.

        Args:
            user_id (str): The ID of the user requesting the recommendation.
            channel_id (str): The ID of the Slack channel containing the
                conversation.
            thread_id (str): The ID of the specific conversation thread.
            max_tokens (int): The maximum number of token that can be parsed
                into the prompt.
        Returns:
            str: The generated recommendation text.
        """
        prompt = self.recommend_ins.get_conversation(user_id=user_id,
                                                     channel_id=channel_id,
                                                     thread_id=thread_id,
                                                     max_tokens=max_tokens)
        return self.recommend_ins.recommend(prompt=prompt)
