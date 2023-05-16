from dataclasses import dataclass


@dataclass
class EmailContainer:
    email_text: str = None
    category: str = None
    summary: str = None
    problem: str = None
    prompt: list[dict[str, str]] = None
