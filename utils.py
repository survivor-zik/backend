from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


def generate_unique_id():
    """Generates a unique ID by combining the current date and time with a random number.

    Returns:
        str: A unique ID string.
    """

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    random_part = str(int(time.time() * 1000) % 1000).zfill(3)  # Pad with zeros
    unique_id = f"{timestamp}{random_part}"
    return unique_id


def send_email(subject: str, body: str, to: str):
    msg = MIMEMultipart()
    msg['From'] = os.getenv("EMAIL_FROM")
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(os.getenv("EMAIL_FROM"), os.getenv("PASS"))
        text = msg.as_string()
        server.sendmail(os.getenv("EMAIL_FROM"), to, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")
