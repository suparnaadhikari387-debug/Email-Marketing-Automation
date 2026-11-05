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

# TEST MODE: True = No real emails sent
TEST_MODE = os.getenv("TEST_MODE", "true").lower() == "true"


def create_email(name, email, template):
    """Create a personalized email."""

    message = EmailMessage()

    message["Subject"] = "Special Updates From Our Team"
    message["From"] = EMAIL_ADDRESS or "test@example.com"
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
    """Prepare or send emails to subscribed contacts."""

    print("\n======================================")
    print("    EMAIL MARKETING AUTOMATION")
    print("======================================")

    if not TEST_MODE:
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            print("ERROR: Email credentials are missing!")
            return

    try:
        # Read email template
        with open(
            "email_template.html",
            "r",
            encoding="utf-8"
        ) as file:
            template = file.read()

        # Read contacts CSV
        with open(
            "contacts.csv",
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            contacts = csv.DictReader(file)

            required_columns = {
                "name", "email", "subscribed"
            }

            if not contacts.fieldnames or not required_columns.issubset(
                contacts.fieldnames
            ):
                print("ERROR: Invalid CSV columns!")
                print("Required: name, email, subscribed")
                return

            total = 0
            prepared = 0
            sent = 0
            skipped = 0
            failed = 0

            # Process each contact
            for contact in contacts:

                total += 1

                name = (contact.get("name") or "").strip()
                email = (contact.get("email") or "").strip()
                subscribed = (
                    contact.get("subscribed") or ""
                ).strip().lower()

                if subscribed != "yes":
                    print(f"SKIPPED: {email}")
                    skipped += 1
                    continue

                if not name or not email:
                    print("FAILED: Missing name or email")
                    failed += 1
                    continue

                try:
                    message = create_email(
                        name, email, template
                    )

                    if TEST_MODE:
                        print(
                            f"TEST: Email prepared for {name} ({email})"
                        )
                        prepared += 1
                        continue

                    # Send real email
                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL(
                        SMTP_SERVER,
                        SMTP_PORT,
                        context=context,
                        timeout=30
                    ) as server:

                        server.login(
                            EMAIL_ADDRESS,
                            EMAIL_PASSWORD
                        )

                        server.send_message(message)

                    print(f"SENT: Email sent to {email}")
                    sent += 1

                except Exception as error:
                    print(f"FAILED: {email} - {error}")
                    failed += 1

            # Display final report
            print("\n======================================")
            print("             FINAL REPORT")
            print("======================================")

            print(f"Total contacts : {total}")
            print(f"Prepared      : {prepared}")
            print(f"Emails sent   : {sent}")
            print(f"Skipped       : {skipped}")
            print(f"Failed        : {failed}")

            print("--------------------------------------")
            print("Email Marketing Automation Completed!")
            print("======================================")

            if TEST_MODE:
                print("MODE: TEST MODE (No emails were sent)")
            else:
                print("MODE: LIVE EMAIL MODE")


    except FileNotFoundError as error:
        print(f"ERROR: Required file not found: {error.filename}")

    except (csv.Error, UnicodeError) as error:
        print(f"ERROR: Could not read project files: {error}")


if __name__ == "__main__":
    send_emails()