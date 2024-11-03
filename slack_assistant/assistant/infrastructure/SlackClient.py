from domain.entities.Thread import Thread
from domain.entities.Message import Message
from slack_bolt import App


class SlackClient:
    """
    A client for interacting with Slack using the Slack Bolt SDK.

    This class provides methods to initialize a connection to Slack,
    retrieve thread information, and reply to threads.

    Attributes:
        app (slack_bolt.App): The Slack Bolt App instance.

    Methods:
        __init__(token: str): Initialize the SlackClient with a Slack API
            token.
        get_thread(channel_id: str, thread_id: str) -> Thread: Retrieve a
            thread from a Slack channel.
        reply_thread(channel_id: str, thread_id: str, text: str) -> None:
            Reply to a thread in a Slack channel.
    """

    def __init__(self, token: str):
        """
        Initialize the SlackClient with a Slack API token.

        This method sets up the Slack Bolt App instance using the provided
        token.

        Args:
            token (str): The Slack API token used for authentication.

        Attributes:
            app (slack_bolt.App): The initialized Slack Bolt App instance.

        Note:
        ___
            The token should have the necessary permissions to perform
            the operations required by other methods in this class.
        """
        self.app = App(token=token)
        self.token = token

    def get_thread(self, channel_id: str, thread_id: str) -> Thread:
        """
        Retrieve raw payload from a thread of a Slack channel

        Args:
            channel_id (str): The ID of the Slack channel.
                Likely to be 'channel' field in payload
            thread_id (str): The ID of the thread.
                Likely to be 'thread_ts' field in payload

        Returns:
            Thread: Thread object including list of messages, channel id,
                thread_id.
        """
        response = self.app.client.conversations_replies(token=self.token,
                                                         channel=channel_id,
                                                         ts=thread_id)
        thread_messages_list = list()
        for message in response['messages']:
            user = message['user']
            text = message['text']
            files = None
            if ('files' in message):
                files = message['files']
            m = Message(user=user, text=text, attachment=files)
            thread_messages_list.append(m)
        result_thread = Thread(
            channel=channel_id,
            thread_ts=thread_id,
            messages=thread_messages_list)

        return result_thread

    def reply_thread(self, user_id: str, channel_id: str,
                     thread_id: str, text: str) -> None:
        """
        Reply to a thread in a Slack channel.

        Args:
            user_id (str): Only this user can see the message
            channel_id (str): The ID of the Slack channel.
            thread_id (str): The ID of the thread.
            text (str): The text of the reply message.
        """
        self.app.client.chat_postEphemeral(
            token=self.token,
            user=user_id,
            channel=channel_id,
            thread_ts=thread_id,
            text=text
        )
