import streamlit as st


def main():
    st.set_page_config(page_title="Hack4Wroclaw App", page_icon=":cat:")
    st.title("Demo App")
    text_input = st.text_input(
        "Enter your name 👇",
        placeholder="Emilka",
    )

    if text_input:
        st.write(f"Hello {text_input}, have a nice day !")


if __name__ == "__main__":
    main()
