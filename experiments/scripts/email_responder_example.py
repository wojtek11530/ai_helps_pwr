from pprint import pprint

from ai_helps_pwr.email_assistance.email_responder import EmailResponder

email_text = """Dzień dobry,
nazywam się Michał i skończyłem studia pierwszego i drugiego stopnia na PWR.
Teraz w październiku zaczynam kolejne studia magisterskie na PWR i
chciałbym się dowiedzieć, czy w związku z tym jestem zobligowany do
ponownego zaliczenia kursów językowych, czy jest możliwość przepisu ocen?
Z wyrazami szacunku,
Michał
"""


def main():
    """Main function of email responder example."""
    responder = EmailResponder()
    response = responder.generate_response(email_text)

    print("Email and response:")
    pprint(vars(response))


if __name__ == "__main__":
    main()
