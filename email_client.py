import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

def send_message(email, to, message, password):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, to, message)
