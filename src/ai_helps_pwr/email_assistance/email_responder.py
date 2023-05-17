"""Email responder."""
import json
from typing import Any

from ai_helps_pwr.email_assistance.email_categories import CATEGORIES
from ai_helps_pwr.email_assistance.email_container import EmailContainer
from ai_helps_pwr.logger import custom_logger
from ai_helps_pwr.models import ChatGPT
from ai_helps_pwr.settings import DATA_DIR
from ai_helps_pwr.utils.common import get_openai_api_key

logger = custom_logger("EmailResponder")

GPT_WHO_YOU_ARE = (
    "Jesteś osobą pracującą w dziekanacie"
    "na wydziale W13 i pomagasz studentom."
)

MSG_TYPE = dict[str, str]
PROMPT_TYPE = list[MSG_TYPE]


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

        prompt = self._generate_first_prompt(email_text)
        response = self._call_gpt_and_get_json_response(prompt)

        problem_category = self._validate_category(
            response.get("problem", None)
        )
        email_response_container.problem = problem_category

        if "summary" in response:
            email_response_container.summary = response["summary"]

        prompt.append(self._pack_chatgpt_response_into_message(response))

        problem_category = email_response_container.problem
        information_to_add = self._determine_information_to_add(
            problem_category
        )
        query_for_answer = self._get_message_quering_for_email_answer(
            information_to_add
        )
        prompt.append(query_for_answer)

        email_response_container.prompt = prompt

        chat_response = self._call_chatgpt(prompt)
        response = self._get_content_from_chatgpt_response(chat_response)
        email_response_container.response = response

        return email_response_container

    def _generate_first_prompt(self, mail_text: str) -> PROMPT_TYPE:
        """Create first prompt. It includes system content and q&A example."""
        system = {"role": "system", "content": GPT_WHO_YOU_ARE}
        user_question_first_prompt = (
            self._get_message_quering_for_email_category_and_summary(
                "Mam problem z XYZ."
            )
        )
        assistant_content = """
         {
         "problem": "inne",
         "summary": "Mail zawiera opis problemu związanego z X."
         }
         """.replace(
            "\n", ""
        )
        assistant_answer_first_prompt = {
            "role": "assistant",
            "content": assistant_content,
        }
        user_question_mail = (
            self._get_message_quering_for_email_category_and_summary(mail_text)
        )
        return [
            system,
            user_question_first_prompt,
            assistant_answer_first_prompt,
            user_question_mail,
        ]

    def _call_gpt_and_get_json_response(self, prompt: PROMPT_TYPE) -> dict:
        """Send prompt send to ChatGPT and transform JSON format response."""
        chat_response = self._call_chatgpt(prompt)
        response_content = self._get_content_from_chatgpt_response(
            chat_response
        )

        response_content = response_content[: response_content.find("}") + 1]
        try:
            response_as_dict = json.loads(response_content)
        except json.decoder.JSONDecodeError:
            response_as_dict = {
                "problem": "inne",
                "summary": "niestandardowy problem",
            }
        return response_as_dict

    def _pack_chatgpt_response_into_message(
        self, response: dict[str, str]
    ) -> MSG_TYPE:
        """Pack intermediary chatgpt response into message.

        It will be used in the final prompt including first prompt and chat gpt
         response with email summary and problem type.
        """
        assistant_response = str(response).replace("'", '"')
        return {"role": "user", "content": assistant_response}

    def _get_message_quering_for_email_category_and_summary(
        self, mail_text: str
    ) -> MSG_TYPE:
        """Create user content used to prompt."""
        categories = str(list(CATEGORIES.keys()))
        content = (
            f'Opisz problem zawarty w mailu: "{mail_text}".'
            "Napisz podsumowanie oraz zaklasyfikuj problem do klasy"
            f"jednej z {categories}."
            'Zwróć w formacie JSON: {"problem", "summmary"}.'
        )

        return {"role": "user", "content": content}

    def _validate_category(self, category: str):
        # In the case when ChatGPT do not return any category or category is
        # incorrect we assign it to category `others` (inne)
        if category is None or category not in CATEGORIES:
            category = "inne"

        return category

    def _determine_information_to_add(self, category: str) -> str:
        category_dict = CATEGORIES[category]
        link = category_dict.get("link", None)
        if link is not None:
            return (
                f"Dziękujemy za zadanie pytania. Proszę sprawdzić, czy "
                f"odpowiedzi na pytanie nie jest Pan/Pani w stanie znaleść na "
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
    ) -> MSG_TYPE:
        with open(
            DATA_DIR / "email_generation_prompt.txt", "r", encoding="utf8"
        ) as f:
            lines = f.readlines()

        prompt_template = "".join(lines).strip()
        return {
            "role": "user",
            "content": prompt_template.format(info=information_to_add),
        }

    def _call_chatgpt(self, prompt: PROMPT_TYPE) -> dict[str, Any]:
        logger.info("Prompt send to ChatGPT")
        chat_response = self._chat_gpt_model(prompt)
        logger.info("Response received from ChatGPT")
        return chat_response

    def _get_content_from_chatgpt_response(
        self, chat_response: dict[str, Any]
    ) -> str:
        return chat_response["choices"][0]["message"]["content"]
