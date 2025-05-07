import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Optionally load from .env
from dotenv import load_dotenv
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email_to_venue(email, venue_name, question, use_mock=True):
    """
    Sends an email to a venue and returns the response (simulated or real).
    Set use_mock=False to send real emails.
    """

    if use_mock:
        print(f"[MOCK EMAIL] Sent to {email}: {question}")
        return f"""
        Hello,

        Thank you for your interest in {venue_name}. We can host up to 150 guests.
        Pricing starts at €5,000 and includes catering, ceremony space, and a DJ.
        Let us know if you’d like a brochure.

        Best,
        The {venue_name} Team
        """

    # --- Real Email Sending ---
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = f"Wedding Venue Inquiry: {venue_name}"

    body = f"""
Dear {venue_name} team,

We are currently building an AI-powered wedding planning assistant, and we’d like to gather some details about your venue:

- Guest capacity
- Pricing tiers
- Availability
- Included services

Please respond with a brochure or answers if possible.

Best regards,
Wedding AI Team
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, email, text)
        server.quit()
        return "Email sent successfully. Awaiting response."
    except Exception as e:
        return f"Email failed: {str(e)}"
