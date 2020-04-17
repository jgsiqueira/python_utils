import smtplib, ssl, random, csv

def send_email(subject, body, from_email, from_password, to_email):
    port = 465
    smtp_server = "smtp.gmail.com"

    message = "Subject: " + subject + "\n\n"
    message += body

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, message.encode("ascii", errors="ignore"))
