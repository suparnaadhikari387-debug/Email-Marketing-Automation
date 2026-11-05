import csv
import os
import ssl
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Keep True while testing
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"


def create_email(name, email, template):

    message = EmailMessage()

    message["Subject"] = "Special Updates From Our Team"
    message["From"] = EMAIL_ADDRESS
    message["To"] = email

    html_content = template.format(name=name)

    message.set_content(
        f"Hello {name}! Thank you for subscribing."
    )

    message.add_alternative(
        html_content,
        subtype="html"
    )

    return message


def send_emails():

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email credentials are missing!")
        return

    with open("email_template.html", "r",
              encoding="utf-8") as file:
        template = file.read()

    with open("contacts.csv", "r",
              newline="", encoding="utf-8") as file:

        contacts = csv.DictReader(file)

        for contact in contacts:

            name = contact["name"]
            email = contact["email"]
            subscribed = contact["subscribed"].lower()

            if subscribed != "yes":
                print(f"Skipped: {email}")
                continue

            message = create_email(
                name, email, template
            )

            if TEST_MODE:
                print(f"TEST: Email prepared for {name}")
                continue

            try:
                context = ssl.create_default_context()

                with smtplib.SMTP_SSL(
                    SMTP_SERVER, SMTP_PORT,
                    context=context
                ) as server:

                    server.login(
                        EMAIL_ADDRESS,
                        EMAIL_PASSWORD
                    )

                    server.send_message(message)

                print(f"Email sent to {email}")

            except Exception as error:
                print(f"Failed for {email}: {error}")


if __name__ == "__main__":
    send_emails()