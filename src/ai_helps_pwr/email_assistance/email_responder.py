"""Email responder."""
from ai_helps_pwr.email_assistance.email_categories import CATEGORIES
from ai_helps_pwr.email_assistance.email_container import EmailContainer
from ai_helps_pwr.logger import custom_logger
from ai_helps_pwr.models import ChatGPT
from ai_helps_pwr.utils.common import get_openai_api_key

prompt_template = """
Jesteś pracownikiem dziekanatu Wydziału Matematyki na Politechnice
Wrocławskiej. Twoim zadaniem jest udzielać pomocy studentom. Wygeneruj
odpowiedź na mejl studenta do dziekanatu, która będzie:
 - informować, żeby spróbował znaleść odpowiedź pod adresem {link}
 - prosić o ponowne zapytanie, jeśli student nie znalazł odpowiedzi na
 jego pytanie.
 - podpisz się jako automatyczny asystent dziekanatu
Treść mejla: {email_text}"""

logger = custom_logger(__name__)


class EmailResponder:
    """Responder to email of students."""

    def __init__(self):
        """Construct Email Responder object."""
        self._api_key = get_openai_api_key()
        self._chat_gpt_model = ChatGPT(
            name="email_response_gpt",
            gpt_model_name="gpt-3.5-turbo",
            key=self._api_key,
        )

    def generate_response(self, email_text: str) -> EmailContainer:
        """Generate response for given student mail."""
        email_response_container = EmailContainer()
        email_response_container.email_text = email_text

        prompt = self._generate_prompt(email_text)

        logger.info("Prompt send to ChatGPT")
        chat_response = self._chat_gpt_model(prompt)
        logger.info("Response received from ChatGPT")

        response = chat_response["choices"][0]["message"]["content"]

        email_response_container.response = response

        return email_response_container

    def _generate_prompt(self, prompt_text: str) -> list[dict[str, str]]:
        prompt = []

        # TODO `category` na razie jako placeholder, należy dodać metodę by
        #  utworzyć pierwsze zapytanie
        # do chata i z niego wyciągnąć preydkowaną kategorię
        category = "zapisy"
        info_to_add = CATEGORIES[category]["info"]

        prompt.append(self._get_message_quering_form_email_answer(info_to_add))
        return [
            {"role": "user", "content": prompt_text},
        ]

    def _get_message_quering_form_email_answer(
        self, info: str
    ) -> dict[str, str]:
        return {"role": "user", "content": prompt_template.format(info=info)}
