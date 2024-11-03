from pydantic import BaseModel
from .Message import Message
from typing import List


class Thread(BaseModel):
    """
    Represents a thread in a chat system.

    This model defines the basic structure of a thread, including
    the channel it belongs to and its timestamp.

    Attributes:
        channel (str): The identifier of the channel where the thread exists.
        thread_ts (str): The timestamp that uniquely identifies the thread.
        messages (List[Message]): Messages inside the thread

    """

    channel: str
    thread_ts: str
    messages: List[Message]
