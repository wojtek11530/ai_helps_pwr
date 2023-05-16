"""Email responder."""
from ai_helps_pwr.email_assistance.email_categories import CATEGORIES
from ai_helps_pwr.email_assistance.email_classificator import EmailClassificator
from ai_helps_pwr.models import ChatGPT
from ai_helps_pwr.utils.common import get_openai_api_key

prompt_template = """
Jesteś pracownikiem dziekanatu Wydziału Matematyki na Politechnice Wrocławskiej. Twoim
zadaniem jest udzielać pomocy studentom. Wygeneruj odpowiedź na mejl studenta do
dziekanatu, która będzie:
 - informować, żeby spróbował znaleść odpowiedź pod adresem {link}
 - prosić o ponowne zapytanie, jeśli student nie znalazł odpowiedzi na jego pytanie.
Treść mejla: {email_text}"""


class EmailResponder:
    """Responder to email of students."""

    def __init__(self):
        """Construct Email Responder object."""
        self._api_key = get_openai_api_key()
        self._classificator = EmailClassificator()
        self._chat_gpt_model = ChatGPT(
            name="email_response_gpt", gpt_model_name="gpt-3.5-turbo", key=self._api_key
        )

    def generate_response(self, email_text: str) -> str:
        """Generate response for given student mail."""
        email_class = self._classificator.classify(email_text)
        link = CATEGORIES[email_class]["link"]

        prompt_text = prompt_template.format(link=link, email_text=email_text)
        prompt = self._generate_prompt(prompt_text)
        chat_response = self._chat_gpt_model(prompt)
        response = chat_response["choices"][0]["message"]["content"]
        response += "\n\n**Odpowiedź wygenerowana automatycznie przy pomocy ChatGPT."
        return response

    @staticmethod
    def _generate_prompt(prompt_text: str) -> list[dict[str, str]]:
        return [
            {"role": "user", "content": prompt_text},
        ]
