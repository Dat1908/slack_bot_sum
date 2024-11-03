from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for Large Language Models (LLMs).

    Provides a common interface for interacting with different
    LLM implementations.
    Subclasses must implement the `invoke` method.
    """

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """
        Invokes the LLM with the given prompt.

        Args:
            prompt (str): The input prompt for the LLM.

        Returns:
            str: The LLM's response to the prompt.

        Raises:
            NotImplementedError: If this method is not implemented by a
            subclass.
        """
        raise NotImplementedError
