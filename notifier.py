"""File to send emails via SMTP."""

import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv
from db import get_email

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465 # Gmail

GMAIL_SENDER = os.getenv("GMAIL_SENDER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Prevent None type during login
if not GMAIL_SENDER or not GMAIL_APP_PASSWORD:
    raise RuntimeError("GMAIL_SENDER and GMAIL_APP_PASSWORD must be set in your .env file")

def send_notification(show_title: str,
                    season_number: int,
                    episode_number: int,
                    episode_title: str) -> None:
    """Sends an email notifying the user of a new episode."""

    recipient_email = get_email()

    if not recipient_email:
        print("No notify email set — skipping notification.")
        return

    subject = f"New episode of {show_title}!"
    body = (
        f"{show_title} just got a new episode:\n\n"
        f"Season {season_number}, Episode {episode_number}: {episode_title}"
    )

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = str(GMAIL_SENDER)
    message["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(str(GMAIL_SENDER), str(GMAIL_APP_PASSWORD))
            server.sendmail(str(GMAIL_SENDER), recipient_email, message.as_string())
    except smtplib.SMTPException as exception:
        print(f"Failed to send notification for {show_title}: {exception}")
