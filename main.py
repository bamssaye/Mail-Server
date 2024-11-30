from concurrent.futures import ThreadPoolExecutor, as_completed
import time,logging
import send_smtp as se
import utils as ut
import send_mx as mx

def main():
    choice = input("Choose sending method (1 for MX, 2 for SMTP): ").strip()
    while choice not in ('1', '2'):
        print("Invalid choice. Please select 1 or 2.")
        choice = input("Choose sending method (1 for MX, 2 for SMTP): ").strip()
    send_func = mx.send_mx if choice == '1' else se.send_smtp
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for batch in se.batches:
            futures.append(executor.submit(send_func, batch, se.from_email))
            time.sleep(1)
        success_emails = []
        error_emails = []
        for future, batch in zip(as_completed(futures), se.batches):
            try:
                result = future.result()
                if result:
                    success_emails.extend(batch)
                else:
                    error_emails.extend(batch)
            except Exception as exc:
                logging.error(f"Batch generated an exception: {exc}")
                error_emails.extend(batch)
        if success_emails:
            ut.log_email('log/email_sended.txt', success_emails)
        if error_emails:
            ut.log_email('log/error_sended.txt', error_emails)
        remaining_emails = [email for email in se.email_list if email not in (success_emails + error_emails)]
        ut.update_email_list_file('Msg/emails-insta.txt', remaining_emails)

if __name__ == '__main__':
    main()