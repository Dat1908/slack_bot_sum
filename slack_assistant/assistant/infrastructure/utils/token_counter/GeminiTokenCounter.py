from .BaseTokenCounter import BaseTokenCounter
from vertexai.preview import tokenization


class GeminiTokenCounter(BaseTokenCounter):
    """
    Counts tokens for Gemini models using Vertex AI's tokenization service.

    Inherits from the BaseTokenCounter class and provides a specific
    implementation for Gemini models.
    """

    def count_tokens(prompt: str, model_name: str) -> int:
        """
        Counts the number of tokens in a given prompt for a Gemini model.

        Args:
            prompt (str): The input text to be tokenized.
            model_name (str): The name of the Gemini model.

        Returns:
            int: The total number of tokens in the prompt.
        """
        tokenizer = tokenization.get_tokenizer_for_model(model_name)
        result = tokenizer.count_tokens(prompt)
        return int(result.total_tokens)
