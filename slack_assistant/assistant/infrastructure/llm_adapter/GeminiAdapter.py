from .BaseLLM import BaseLLM
import google.generativeai as genai


class GeminiAdapter(BaseLLM):
    """
    Adapter class for interacting with Google's Gemini LLM through the
    google.generativeai library.

    Inherits from the BaseLLM class and provides an implementation of the
    `invoke` method.
    """

    def __init__(self, key: str, model_name: str):
        """
        Initializes the GeminiAdapter with the provided API key and model name.

        Args:
            key (str): The API key for accessing the Gemini LLM.
            model_name (str): The name of the Gemini LLM model to use.
        """
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel(model_name=model_name)

    def invoke(self, prompt: str) -> str:
        """
        Invokes the Gemini LLM with the given prompt.

        Args:
            prompt (str): The input prompt for the LLM.

        Returns:
            str: The Gemini LLM's response to the prompt.
        """
        response = self.model.generate_content(prompt)
        return response
