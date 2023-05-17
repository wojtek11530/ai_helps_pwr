from dataclasses import dataclass


@dataclass
class EmailContainer:
    """Construct Email Container object."""

    email_text: str = None
    summary: str = None
    problem: str = None
    full_problem_name: str = None
    response: str = None
    prompt: list[dict[str, str]] = None
