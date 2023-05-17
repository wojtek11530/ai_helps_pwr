"""Demo using streamlit."""
import streamlit as st

from ai_helps_pwr.email_assistance.email_responder import EmailResponder


def main():
    """Demo App."""
    st.set_page_config(page_title="GPT Asystent dziekaantu", page_icon=":cat:")
    st.title("Asystent dziekanatu")

    for state_variable in ["student_mail", "mail_response"]:
        if state_variable not in st.session_state:
            st.session_state[state_variable] = ""

    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    responder = EmailResponder()

    text_input = st.text_area(
        "Mejl studenta 👇", height=250, value=st.session_state.student_mail
    )
    _, middle_col, _ = st.columns([2, 3, 2])

    button_disabled = len(text_input) == 0 or st.session_state.disabled
    button = middle_col.button(
        "Generuj odpowiedź",
        disabled=button_disabled,
        use_container_width=True,
        on_click=_disable_button,
        type="primary",
    )

    if button:
        with st.spinner("Generowanie mejla z odpowiedzią, proszę czekać..."):
            response = responder.generate_response(text_input)
        st.session_state.mail_response = response.response
        _enable_button()
        st.experimental_rerun()
    else:
        if len(st.session_state.mail_response) > 0:
            st.write("Automatyczna odpowiedź:")
            st.write(st.session_state.mail_response)


def _disable_button():
    st.session_state.disabled = True


def _enable_button():
    st.session_state.disabled = False


if __name__ == "__main__":
    main()
