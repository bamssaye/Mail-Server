import logging,smtplib, dns.resolver, socket
from email.mime.multipart import MIMEMultipart
from header import EmailHeaderManager

def get_mx_records(domain):
    records = dns.resolver.resolve(domain, 'MX')
    mx_records = sorted(records, key=lambda record: record.preference)
    return [str(record.exchange) for record in mx_records]
#/////////////////////////////////////////
def get_ipv4_address(hostname):
    try:
        addrinfo = socket.getaddrinfo(hostname, None, socket.AF_INET)
        return addrinfo[0][4][0]  # Return first IPv4 address
    except Exception as e:
        logging.error(f"Failed to resolve IPv4 for {hostname}: {e}")
        return None
#/////////////////////////////////////////
def send_mx(to_emails, from_email):
    if not to_emails:
        return
    domain = to_emails[0].split('@')[1]
    mx_records = get_mx_records(domain)
    header = EmailHeaderManager()
    msg = MIMEMultipart('alternative')
    msg = header.add_headers_to_message(msg)
    msg['To'] = from_email[0]
    msg['Bcc'] = ', '.join(to_emails)
    for mx in mx_records:
        try:
            ipv4_addr = get_ipv4_address(mx)
            if not ipv4_addr:
                continue
            with smtplib.SMTP(ipv4_addr) as server:
                server.sendmail(from_email, to_emails, msg.as_string())
                logging.info(f"Batch of {len(to_emails)} emails sent successfully via {mx}")
                return True
        except Exception as e:
            logging.error(f"Failed to send batch of {len(to_emails)} emails via {mx}: {e}")
            return False
##/////////////////////////////////////////
