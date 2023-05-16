from dataclasses import dataclass


@dataclass
class EmailContainer:
    """Construct Email Container object."""

    email_text: str = None
    category: str = None
    summary: str = None
    problem: str = None
    response: str = None
    prompt: list[dict[str, str]] = None

    def __repr__(self):
        """Return string representation of email."""
        return (
            f"{self.__class__.__name__}\n"
            f"email_text={self.email_text}\n"
            f"category={self.category}\n"
            f"summary={self.summary}\n"
            f"response={self.response}\n"
        )
