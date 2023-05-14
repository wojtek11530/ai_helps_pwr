import click
from streamlit.web.cli import _main_run

from streamlit_demo_app import demo_app


@click.command(context_settings={"show_default": True})
def main():
    filename = demo_app.__file__
    _main_run(filename)


if __name__ == "__main__":
    main()
