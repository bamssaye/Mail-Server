import smtplib
from email.mime.multipart import MIMEMultipart
from header import EmailHeaderManager
import utils as ut

#/////////////////////////////////////////
from_email = ut.read_email_list('Msg/from_email.txt')
email_list = ut.read_email_list('Msg/mails-insta.txt')
batches = list(ut.batch_email_list(email_list, 2))
#/////////////////////////////////////////
def send_smtp(to_emails, from_email):
    if not to_emails:
        return
    login, passw, port, hostr = open("info/smtp.txt").readline().strip().split('|')
    with open('info/dk.pem', 'r') as f:dk = f.read()
    if not all([login, passw, port, hostr]): return
    port = int(port)
    header = EmailHeaderManager()
    msg = MIMEMultipart('alternative')
    msg = header.add_headers_to_message(msg)
    #msg['Bcc'] = ', '.join(to_emails)
    msg['To'] = to_emails[0]
    message_str = msg.as_string()
    msg_dkim = ut.generate_dkim(dk,"key",message_str,header,from_email) + message_str
    try:
        with smtplib.SMTP(hostr, port) as server:
            server.login(login, passw)
            server.sendmail(from_email, to_emails, msg_dkim)
            print("Email Sent...")
            return True  
    except Exception as e:
        print(f"Send failed: {e}")
        return False
# /////////////////////////////////////////////

