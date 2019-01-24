from flask_mail import Mail, Message 
mail=Mail()
from os import environ
def send_mail_notification(**message): 
    subject = message['title'] +" << STATUS Updated >>"
    sender = environ.get("MAIL_USERNAME")
    msg = Message(subject, sender = 'eliatboot@gmail.com', recipients = [message["email"]])
    msg.body = "Hello {}, Your incident - {} has been updated to {} ".format(message["by_name"],\
                message["comment"],message["status"])
    mail.send(msg) 