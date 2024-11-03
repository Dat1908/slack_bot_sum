from infrastructure.llm_adapter.GeminiAdapter import GeminiAdapter
from .prompt import classify_prompt
import json


class ClassifyRequest:
    """
    A class to classify user requests using the Gemini language model.

    This class initializes a GeminiAdapter and provides a method to \
    classify
    user input text into predefined categories.

    Attributes:
        llm_adapter (GeminiAdapter): An adapter for interacting with the \
        Gemini language model.

    Methods:
        classify: Classifies the given text input into predefined \
        categories.
    """

    def __init__(self,
                 llm_token: str,
                 model_name: str = "gemini-1.5-flash"):
        """
        Initializes the ClassifyRequest instance with a Gemini language model \
        adapter.

        Args:
            llm_token (str): Authentication token for the Gemini language \
            model.
            model_name (str, optional): Name of the Gemini model to use. \
            Defaults to "gemini-1.5-flash".
        """
        llm_adapter = GeminiAdapter(key=llm_token, model_name=model_name)
        self.llm_adapter = llm_adapter

    def classify(self, text: str) -> dict:
        """
        Classifies the given text input into predefined categories.

        This method sends the input text to the Gemini model for classification
        and returns the result as a dictionary.

        Args:
            text (str): The user input text to be classified.

        Returns:
            dict: A dictionary containing the classification results.
                  Expected format: {"summarize": int, "recommend": int},
                  where int is either 0 (false) or 1 (true).
        Raises:
            json.JSONDecodeError: Error if LLM doesn't return the right JSON\
                format
        """
        prompt = classify_prompt.format(user_input=text)
        respond = self.llm_adapter.invoke(prompt)
        json_output = respond.text
        try:
            result = json.loads(json_output)
            return result
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None  # or return a default value, or re-raise the exception
