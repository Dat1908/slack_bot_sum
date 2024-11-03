from infrastructure.utils.token_counter.GeminiTokenCounter import (
    GeminiTokenCounter
)
from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
from infrastructure.SlackClient import SlackClient
from domain.entities.Thread import Thread
from .prompt import recommend_prompt
from copy import deepcopy
import re


class Recommend:
    """
    A class to generate recommendations based on Slack conversations.

    Attributes:
        llm_adapter (GeminiAdapter): An adapter for the Gemini language model.
        slack_client (SlackClient): A client for interacting with the Slack
            API.
        model_name (str): Name of the LLM used for generating text, by default
            using `gemini-1.5-flash`.

    Methods:
        get_conversation: Retrieves and formats a conversation from Slack.
        recommend: Generates a recommendation based on the conversation.
    """

    def __init__(self, slack_bot_token: str,
                 llm_token: str,
                 model_name: str = "gemini-1.5-flash"):
        """
        Initializes the Recommend instance.

        Args:
            slack_bot_token (str): Slack bot token to init SlackClient
                instance - which is responsible for getting thread messages
                and posting messages.
            llm_token (str): LLM token to init LLM adapters.
        model_name (str): Name of the LLM used for generating text, by default
            using `gemini-1.5-flash`.
        """
        llm_adapter = GeminiAdapter(key=llm_token, model_name=model_name)
        slack_client = SlackClient(token=slack_bot_token)
        self.llm_adapter = llm_adapter
        self.slack_client = slack_client
        self.model_name = model_name

    def __map_user(self, thread: Thread) -> dict:
        """
        Create a mapping of user IDs to anonymized user names.

        This method processes a Thread object,
        mapping each unique user ID to an
        anonymized name (e.g., "User1", "User2", etc.).
        It considers both the message
        senders and any users mentioned in the message text.

        Args:
            thread (Thread): The Thread object
                containing messages to be processed.

        Returns:
            dict: A dictionary mapping original user IDs to
                anonymized user names.

        Note:
            - User IDs in message text are expected\
            to be in the format "<@Uxxxxxxxx>".
            - The anonymized names start from "User1"\
            and increment for each new user.
        """
        user_map = dict()
        messages = thread.messages
        user_index = 1  # Mapping starts with User1
        user_id_regex = "<@U[a-zA-Z0-9]+>"
        for message in messages:
            # Start adding from Message.user
            if message.user not in user_map:
                user_map[message.user] = f"User{user_index}"
                user_index += 1
            # Find mentioned users in message text and remove additional chars
            user_id_match_list = [s[2:-1]
                                  for s in re.findall(user_id_regex,
                                                      message.text)]
            # Add valid user_id into user_map
            for user_id in user_id_match_list:
                if user_id not in user_map:
                    user_map[user_id] = f"User{user_index}"
                    user_index += 1
        return user_map

    def __change_id(self, thread: Thread, user_map: dict) -> Thread:
        """
        Apply user ID anonymization to a Thread object.

        This method creates a deep copy of the
        input Thread object and replaces all
        user IDs (both message senders and mentions in message text)
        with their corresponding anonymized names from the user_map.

        Args:
            thread (Thread): The original Thread object to be anonymized.
            user_map (dict): A dictionary mapping original user IDs to\
                anonymized names.

        Returns:
            Thread: A new Thread object with anonymized user IDs.

        Note:
            - This method does not modify the original Thread object.
            - User mentions in message text are expected to be in the format\
                "<@Uxxxxxxxx>".
        """
        cloned_thread = deepcopy(thread)
        user_id_regex = "<@U[a-zA-Z0-9]+>"
        for message in cloned_thread.messages:
            message.user = user_map[message.user]
            text = message.text
            user_id_match_list = [s[2:-1]
                                  for s in re.findall(user_id_regex,
                                                      text)]
            for user_id in user_id_match_list:
                text = re.sub(user_id, user_map[user_id], text)
            message.text = text
        return cloned_thread

    def get_conversation(self, user_id: str,
                         channel_id: str,
                         thread_id: str,
                         max_tokens: int) -> str:
        """
        Retrieves a conversation from Slack and formats it for the
            recommendation prompt.

        Args:
            user_id (str): The ID of the user requesting the recommendation.
            channel_id (str): The ID of the Slack channel containing the
                conversation.
            thread_id (str): The ID of the specific conversation thread.
            max_tokens (int): The maximum number of tokens allowed in the
                prompt.

        Returns:
            str: A formatted prompt containing the conversation history.
        """
        thread = self.slack_client.get_thread(
            channel_id=channel_id, thread_id=thread_id)

        # Init user mapping
        user_map = self.__map_user(thread=thread)
        if (user_id not in user_map):
            user_map[user_id] = f"User{len[user_map + 1]}"
        converted_thread = self.__change_id(thread=thread, user_map=user_map)
        prompt = recommend_prompt.format(user_id=user_map[user_id])

        # Components to store messages and calculate tokens
        convesation_list = list()  # temp list to store latest messages
        messages_list = converted_thread.messages
        no_of_token = GeminiTokenCounter.count_tokens(
            prompt=prompt, model_name="gemini-1.5-flash")

        # Begin from latest messages
        for message in messages_list[::-1]:
            # Create user-message pair
            user_message = f"{message.user}: {message.text}"
            user_message_token = GeminiTokenCounter.count_tokens(
                prompt=user_message, model_name="gemini-1.5-flash")
            if no_of_token + user_message_token > max_tokens:
                break
            else:
                convesation_list.append(user_message)
                no_of_token += user_message_token

        # Revert latest messages to original timeline
        for user_message in convesation_list[::-1]:
            prompt += f"{user_message}\n"
        return prompt

    def recommend(self, prompt) -> str:
        """
        Generates a recommendation based on the provided conversation prompt.

        Args:
            prompt (str): The formatted conversation prompt.

        Returns:
            str: The generated recommendation text.
        """
        respond = self.llm_adapter.invoke(prompt=prompt)
        return respond.text
