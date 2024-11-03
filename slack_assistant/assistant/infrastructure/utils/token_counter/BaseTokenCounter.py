from abc import ABC, abstractmethod


class BaseTokenCounter(ABC):
    """
    Abstract base class for token counting.

    Provides a common interface for different token counting implementations.
    Subclasses must implement the `count_tokens` method.
    """

    @abstractmethod
    def count_tokens(self, prompt: str, model_name: str) -> int:
        """
        Counts the number of tokens in a given prompt for a specific model.

        Args:
            prompt (str): The input text to be tokenized.
            model_name (str): The name of the language model.

        Returns:
            int: The number of tokens in the prompt.

        Raises:
            NotImplementedError: If this method is not implemented by a
            subclass.
        """
        raise NotImplementedError
