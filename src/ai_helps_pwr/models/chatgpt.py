"""GPT Api connection."""
from typing import Any

import openai


class ChatGPT:
    """Model to conversation."""

    def __init__(self, name: str, gpt_model_name: str, key: str):
        """Init."""
        self.name = name
        self.gpt_model_name = gpt_model_name
        openai.api_key = key
        openai.organization = "bardsai"

    def __call__(self, prompt: list[dict[str, str]]) -> dict[str, Any]:
        """Post prompt to GPT API."""
        return openai.ChatCompletion.create(
            model=self.gpt_model_name, messages=prompt
        )
