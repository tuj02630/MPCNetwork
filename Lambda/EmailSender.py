def send(to_mail, subject, letter_body):
    import os
    import json
    import smtplib
    from email import message

    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    body = json.dumps('Hello from Lambda!')
    try:
        smtp_account_id = os.environ.get('SmtpAccountID', '')
        smtp_account_pass = os.environ.get('SmtpAccountPass', '')

        msg = message.EmailMessage()
        msg.set_content(letter_body);
        msg['Subject'] = subject
        msg['From'] = smtp_account_id
        msg['To'] = to_mail
        print(msg)
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_account_id, smtp_account_pass)
        server.send_message(msg)
        server.quit()
        print("Message sent")
    except Exception as e:
        print(e)
        return False
    else:
        return True