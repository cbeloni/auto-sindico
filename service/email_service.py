import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()

email = os.environ.get('IMAP_EMAIL')
password = os.environ.get('IMAP_PASSWORD')


def read_emails_from_gmail(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    date = (datetime.now() - timedelta(15)).strftime("%d-%b-%Y")        
    status, messages = mail.search(None, f'(UNSEEN SINCE {date} FROM "naoresponda@cora.com.br")')
    email_ids = messages[0].split()
    
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                # Decode the email sender
                from_ = msg.get("From")
                
                print("Subject:", subject)
                print("From:", from_)
                
                # If the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            print("Body:", body)
                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        print("Body:", body)
    
    # Logout and close the connection
    mail.logout()

read_emails_from_gmail(email, password)