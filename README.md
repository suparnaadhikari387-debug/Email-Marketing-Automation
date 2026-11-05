# Email Marketing Automation

This project sends HTML-based email campaigns to contacts listed in a CSV file. It reads subscriber details, loads an email template, and sends personalized emails using Gmail's SMTP server.

## Features

- Reads contacts from a CSV file
- Sends personalized emails with a name field
- Uses an HTML email template
- Filters only subscribed users
- Supports a test mode before sending real emails
- Uses environment variables for secure email credentials

## Project Files

- `main.py` - Main script that reads contacts and sends emails
- `email_template.html` - HTML email body used for the campaign
- `contacts.csv` - Contact list with name, email, and subscription status
- `requirements.txt` - Required Python package(s)
- `.env` - Local environment variables (not committed to version control)

## Requirements

Make sure you have Python 3 installed.

Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Open the project folder.
2. Create a `.env` file in the same directory.
3. Add your Gmail credentials:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TEST_MODE=true
```

### Important note about Gmail

- Use a Google account that allows SMTP access.
- If you use Gmail with 2-Step Verification enabled, generate an App Password and use that instead of your normal account password.
- If `TEST_MODE=true`, the script prepares the emails but does not actually send them.

## CSV Format

The `contacts.csv` file should look like this:

```csv
name,email,subscribed
Rahul,rahul@example.com,yes
Priya,priya@example.com,yes
Amit,amit@example.com,no
```

Only rows where `subscribed` is `yes` are processed.

## Running the Script

From the project folder, run:

```bash
python main.py
```

## How it Works

- Loads environment variables from `.env`
- Reads the HTML email template
- Reads each record from the CSV file
- Checks whether the user is subscribed
- Builds a personalized email message
- Sends the email through Gmail SMTP when not in test mode

## Example Behavior

When `TEST_MODE=true`, output will look similar to:

```text
TEST: Email prepared for Rahul
TEST: Email prepared for Priya
Skipped: amit@example.com
```

## Security Tips

- Do not push your `.env` file to GitHub.
- Keep your email credentials private.
- Avoid hardcoding email passwords directly in the code.

## License

This project is intended for educational use and personal experimentation.
