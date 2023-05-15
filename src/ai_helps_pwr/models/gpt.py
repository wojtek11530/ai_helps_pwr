"""GPT Api connection."""
import openai


class GPT:
    """Model to conversation."""

    def __init__(
        self,
        name: str,
        gpt_model_name: str,
    ):
        """Init."""
        self.name = name
        self.gpt_model_name = gpt_model_name

    def __call__(self, prompt, key):
        """Post prompt to GPT API."""
        openai.api_key = key
        return openai.ChatCompletion.create(
            model=self.gpt_model_name,
            messages=prompt
        )
