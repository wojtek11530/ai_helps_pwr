from ai_helps_pwr.email_assistance.email_responder import EmailResponder

email_text = """Dzień dobry,

chciałbym się dowiedzieć czy mogę przepisać się na zajęcia laboratoryjne z
Analizy Matematycznej do grupy pana dra Cichonia w poniedziałki o 17:15 mimo
braku miejsc.

Pozdrawiam
Stefan Banach
"""


def main():
    """Main function of email responder example."""
    responder = EmailResponder()
    response = responder.generate_response(email_text)

    print(f"Email text:\n{email_text}")
    print(f"Generated response:\n{response}")


if __name__ == "__main__":
    main()
