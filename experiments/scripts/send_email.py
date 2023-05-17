"""Script to sending email."""
from pathlib import Path

import click

from ai_helps_pwr.email_assistance.email_sender import EmailSender
from ai_helps_pwr.utils.common import get_email_credentials

text = """Dzień dobry,\n

Przykładowy text\n

Twój Dziekanat
"""


@click.command()
@click.option(
    "--config_path",
    help="Path to config.",
    type=click.Path(exists=True, path_type=Path),
    default=Path("config/config.local"),
)
def main(config_path: Path):
    """Main function of email responder example."""
    sender, password = get_email_credentials(config_path)

    email_sender = EmailSender(sender, password)
    email_sender.send_mail(
        receiver_email="wojtek19962a32@gmail.com", text=text
    )


if __name__ == "__main__":
    main()
