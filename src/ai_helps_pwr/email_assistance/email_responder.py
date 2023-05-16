"""Email responder."""
import json

from ai_helps_pwr.email_assistance.email_categories import CATEGORIES
from ai_helps_pwr.email_assistance.email_container import EmailContainer
from ai_helps_pwr.logger import custom_logger
from ai_helps_pwr.models import ChatGPT
from ai_helps_pwr.settings import DATA_DIR
from ai_helps_pwr.utils.common import get_openai_api_key

logger = custom_logger("EmailResponder")

GPT_WHO_YOU_ARE = "Jesteś osobą pracującą w dziekanacie" \
    "na wydziale W13 i pomagasz studentom."


def user_question(mail_text: str):
    """Create user content used to prompt."""
    categories = str(list(CATEGORIES.keys()))
    content = f"Opisz problem zawarty w mailu: \"{mail_text}\"." \
        "Napisz podsumowanie oraz zaklasyfikuj problem do klasy" \
        f"jednej z {categories} ." \
        "Zwróć w formacie JSON: {\"problem\", \"summmary\"}."

    return {
        'role': 'user', 'content': content
    }


def first_prompt(mail_text: str) -> list[dict[str, str]]:
    """Create first prompt. It includes system content and q&A example."""
    system = {'role': 'system', 'content': GPT_WHO_YOU_ARE}
    user_question_first_prompt = user_question("Mam probelm z XYX.")
    assistant_content = """
     {
     "problem": "inne",
     "summary": "Mail zawiera opis problemu związanego z X."
     }
     """.replace("\n", "")
    assistant_answer_first_prompt = {
        'role': 'assistant',
        'content': assistant_content
    }
    user_question_mail = user_question(mail_text)
    return [
        system,
        user_question_first_prompt,
        assistant_answer_first_prompt,
        user_question_mail
    ]


def create_conversation(
        prompt: list[dict[str, str]],
        response: dict[str, str]
) -> list[dict[str, str]]:
    """Create conversation (prompt).

    Prompt includes base prompt and gpt response.
    """
    assistant_response = str(response).replace("'", '"')
    final_prompt = prompt + [{
        'role': 'user', 'content': assistant_response
    }]
    return final_prompt


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

    def post_gpt(self, prompt):
        """Prompt send to ChatGPT and transform response."""
        logger.info("Prompt send to ChatGPT")
        chat_response = self._chat_gpt_model(prompt)
        logger.info("Response received from ChatGPT")

        response = chat_response["choices"][0]["message"]["content"]
        response = response[:response.find("}") + 1]
        try:
            response = json.loads(response)
        except json.decoder.JSONDecodeError:
            response = {
                'problem': 'inne',
                'summary': 'niestandardowy problem'
            }
        return response

    def generate_response(self, email_text: str) -> EmailContainer:
        """Generate response for given student mail."""
        email_response_container = EmailContainer()
        email_response_container.email_text = email_text

        prompt = first_prompt(email_text)
        response = self.post_gpt(prompt)

        for key in ['problem', 'summary']:
            if key in response:
                email_response_container.key = response[key]

        email_response_container.prompt = create_conversation(
            prompt, response
        )

        return email_response_container

    def _generate_prompt(self, prompt_text: str) -> list[dict[str, str]]:
        prompt = []

        # TODO `category` na razie jako placeholder, należy dodać metodę by
        #  utworzyć pierwsze zapytanie do chata i z niego wyciągnąć predykowaną
        #  kategorię
        category = "zapisy"
        information_to_add = self._determine_information_to_add(category)

        query_for_answer = self._get_message_quering_for_email_answer(
            information_to_add
        )
        prompt.append(query_for_answer)
        return prompt

    def _determine_information_to_add(self, category: str) -> str:
        category_dict = CATEGORIES[category]
        link = category_dict.get("link", None)
        if link is not None:
            return (
                f"Dziękujemy za zadanie pytania. Proszę sprawdzić, czy "
                f"odpowiedzi na pytanie nie jest pan/pani w stanie znaleść na "
                f"stronie:\n{link}.\n"
                f"Jeśli nie udałaby się Panu/Pani odszukać "
                f"szukanych informacji, proszę wysłać zapytanie ponownie, "
                f"na które pracownik dziekanatu udzieli odpowiedzi."
            )

        if "response" in category_dict:
            return category_dict["response"]

        else:
            raise ValueError(
                "Category dict should contain either field"
                " 'link' or 'response`."
            )

    def _get_message_quering_for_email_answer(
        self, information_to_add: str
    ) -> dict[str, str]:
        with open(
            DATA_DIR / "email_generation_prompt.txt", "r", encoding="utf8"
        ) as f:
            lines = f.readlines()

        prompt_template = "".join(lines).strip()
        return {
            "role": "user",
            "content": prompt_template.format(info=information_to_add),
        }
