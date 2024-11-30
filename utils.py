import dkim,logging,re
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
#////////////////////////////////////
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("log/logs.txt"),
                        logging.StreamHandler()
                    ])
#////////////////////////////////////
def log_email(file_path, email_list):
    with open(file_path, 'a', encoding='utf-8') as file:
        for email in email_list:
            file.write(email + '\n')
#////////////////////////////////////
def generate_dkim(dki, key, msg, header, femail):
    try:
        message_bytes = msg.encode('utf-8')
        domain = femail[0].split("@")[1]
        headers = header.get_dkim_headers()
        sig = dkim.sign(
            message=message_bytes,
            selector=key.encode(),
            domain=domain.encode(),
            privkey=dki.encode(),
            include_headers=headers
        )
        return sig.decode('utf-8')
    except Exception as e:
        return logging.error(f"DKIM signing failed: {e}"), False
# /////////////////////////////////////////////
def read_email_list(file_path):
    with open(file_path, 'r') as file:
        emails = [line.strip() for line in file if line.strip()]
    return emails
#////////////////////////////////////
def batch_email_list(email_list, batch_size): 
    for i in range(0, len(email_list), batch_size):
        yield email_list[i:i + batch_size]
#////////////////////////////////////
def update_email_list_file(file_path, remaining_emails):
    with open(file_path, 'w', encoding='utf-8') as file:
        for email in remaining_emails:
            file.write(email + '\n')
#////////////////////////////////////
def replace_placeholders_in_text(text):
    from header import RandomGenerator
    ge = RandomGenerator()
    def replace_match(match):
        pattern = match.group()
        return ge.generate_single(pattern)
    return re.sub(ge.pattern_regex, replace_match, text)
#////////////////////////////////////
def set_content_encode(msg):
    from header import RandomGenerator
    try:
        html = open("Msg/html_type.html", 'r', encoding='utf-8').read()
        text = open("Msg/text_type.txt", 'r', encoding='utf-8').read()
    except Exception as e:
        logging.error(f"Failed to read template: {e}")
        return None
    ge = RandomGenerator()
    text_2 = ge.replace_hexcaracter(replace_placeholders_in_text(text))
    html_2 = ge.replace_hexcaracter(replace_placeholders_in_text(html))
    text_part = MIMEText(text_2, 'plain', 'utf-8')
    html_part = MIMEBase('text', 'html')
    text_part.set_payload(text_2)
    html_part.set_payload(html_2)
    text_part.replace_header('Content-Transfer-Encoding', 'quoted-printable')
    html_part.add_header('Content-Transfer-Encoding', 'quoted-printable')
    msg.attach(text_part)
    msg.attach(html_part)
    return msg