from pydantic import BaseModel, model_validator
from typing import Any, List, Optional


class Message(BaseModel):
    """
    Represents a message in a messaging system.

    This class defines the structure of a message,
    including the sender and various content types.
    It ensures that at least one form of content is provided for each message.

    Attributes:
        user (str): The identifier of the user sending the message.
        attachment (Optional[List]): A list of attachments, if any.
        blocks (Optional[str]): Block content, represented as a string but
            should be in list format.
        text (Optional[str]): The text content of the message.

    Notes
    -----
        At least one of 'attachment', 'blocks', or 'text' must be provided for
        a valid message.
    """
    user: str
    attachment: Optional[List] = None
    blocks: Optional[str] = None
    text: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def check_content_field(cls, data: Any) -> Any:
        """
        Validates that at least one content field is provided.

        This validator ensures that at least one of 'attachment', 'blocks',
        or 'text' is present in the input data.

        Args:
            cls: The class itself (implicitly passed for class methods).
            data (Any): The input data dictionary.

        Returns:
            Any: The validated input data.

        Raises:
            ValueError: If none of the required content fields are provided.
        """
        if not any(data.get(field) for field in ('attachment',
                                                 'blocks',
                                                 'text')):
            raise ValueError(
                "At least attachment, blocks or text must be provided")
        return data
