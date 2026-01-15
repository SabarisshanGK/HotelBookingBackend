# imports
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")

def send_email(to_email: str , subject: str , body: str):
    msg = MIMEMultipart()
    msg["From"] = f"Namma hotel booking service <{SMTP_FROM}>"
    msg["To"] = to_email
    msg["subject"] = subject
    msg["X-Mailer"] = "Namma hotel booking Mail Service"

    msg.attach(MIMEText(body,"html"))

    with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER,SMTP_PASSWORD)
        server.sendmail(from_addr=SMTP_FROM,to_addrs=to_email,msg=msg.as_string())