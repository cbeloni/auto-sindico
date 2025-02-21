import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os
from service.csv_service import read_lines
from repository.extrato import ExtratoRepository
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

extrato_repository = ExtratoRepository()


imap_email = os.environ.get('IMAP_EMAIL')
imap_password = os.environ.get('IMAP_PASSWORD')


def read_emails_from_gmail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(imap_email, imap_password)
    mail.select("inbox")
    date = (datetime.now() - timedelta(15)).strftime("%d-%b-%Y")        
    status, messages = mail.search(None, f'(UNSEEN SINCE {date} FROM "naoresponda@cora.com.br")')
    email_ids = messages[0].split()
    linhas = []
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or 'utf-8')
                
                for file in msg.walk():
                    linhas = read_lines(file)
                
                for linha in linhas:
                    try:
                        extrato_repository.salvar(linha)
                    except Exception as e:
                        logging.info(f"Error ao salvar extrato: {e}")
    
    # Logout and close the connection
    mail.logout()
    return linhas

def enviar_email(subject, body, to_email):
    from_email = imap_email
    password = imap_password

    # Create the email headers and set the subject, from, and to addresses
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    logging.info(f"Email sent to {to_email}")    