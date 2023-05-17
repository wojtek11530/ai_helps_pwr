"""Demo using streamlit."""
import streamlit as st

from ai_helps_pwr.email_assistance.email_responder import EmailResponder
from ai_helps_pwr.email_assistance.email_sender import EmailSender
from ai_helps_pwr.utils.common import get_email_credentials
from streamlit_demo_app.settings import APP_DIR, CONFIG_DIR

EMAIL_RECEIVER = "wojtek19962a32@gmail.com"


def main():
    """Demo App."""
    st.set_page_config(page_title="GPT Asystent dziekanatu", page_icon=":cat:")

    # Load CSS style for markdown elements
    _load_css()

    # Configure state variables
    for state_variable in [
        "student_mail",
        "mail_response",
        "mail_category",
        "mail_summary",
    ]:
        if state_variable not in st.session_state:
            st.session_state[state_variable] = ""

    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    # Create EmailResponder object
    responder = EmailResponder()

    # Create EmailSender object
    config_path = CONFIG_DIR / "config.local"
    sender, password = get_email_credentials(config_path)
    email_sender = EmailSender(sender, password)

    st.title("Asystent dziekanatu")
    st.markdown("**Mejl studenta** 👇")
    text_input = st.text_area(
        "Mejl studenta 👇",
        height=250,
        value=st.session_state.student_mail,
        label_visibility="collapsed",
    )
    _, middle_col, _ = st.columns([2, 3, 2])

    button = middle_col.button(
        "Generuj odpowiedź",
        disabled=st.session_state.disabled,
        use_container_width=True,
        on_click=_disable_button(),
        type="secondary",
    )

    if button:
        if len(text_input) > 0:
            with st.spinner(
                "Generowanie mejla z odpowiedzią, proszę czekać..."
            ):
                (
                    email_response_container,
                    prompt,
                ) = responder.run_auxiliary_gpt_call(text_input)
                st.session_state.mail_category = (
                    email_response_container.full_problem_name
                )
                st.session_state.mail_summary = (
                    email_response_container.summary
                )
                _display_email_data()
                responder.run_final_gpt_call(email_response_container, prompt)

            st.session_state.mail_response = email_response_container.response
            _enable_button()
            st.experimental_rerun()
        else:
            st.info(
                "Pole z mejlem studenta puste, podaj mejl studenta by "
                "móc wygenerować automatyczną odpowiedź.",
                icon="ℹ️",
            )
            _enable_button()
    else:
        if len(st.session_state.mail_response) > 0:
            _display_email_data()
            st.markdown("**Automatyczna odpowiedź:**")
            st.markdown(
                f"<div class='italic'>{st.session_state.mail_response}</div>",
                unsafe_allow_html=True,
            )
            email_sender.send_mail(
                receiver_email=EMAIL_RECEIVER,
                text=st.session_state.mail_response,
            )


@st.cache_resource
def _load_css():
    with open(APP_DIR / "style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def _display_email_data():
    st.markdown(
        f"**Kategoria**: <span class='highlight blue'>"
        f"{st.session_state.mail_category}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**Podsumowanie mejla studenta:** {st.session_state.mail_summary}"
    )


def _disable_button():
    st.session_state.disabled = True


def _enable_button():
    st.session_state.disabled = False


if __name__ == "__main__":
    main()
