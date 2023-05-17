"""Demo using streamlit."""
import streamlit as st

from ai_helps_pwr.email_assistance.email_responder import EmailResponder


def main():
    """Demo App."""
    st.set_page_config(page_title="Hack4Wroclaw App", page_icon=":cat:")
    st.title("Asystent dziekanatu")

    responder = EmailResponder()

    text_input = st.text_area("Mejl studenta 👇", height=250)

    col1, col2, col3 = st.columns([2, 3, 2])

    if col2.button(
        "Generuj odpowiedź",
        disabled=len(text_input) == 0,
        use_container_width=True,
    ):
        response = responder.generate_response(text_input)
        st.write("Automatyczna odpowiedź:")
        st.write(response.response)


if __name__ == "__main__":
    main()
