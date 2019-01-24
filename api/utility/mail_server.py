from flask_mail import Mail, Message 
mail=Mail()

def send_mail_notification(**message): 
    subject = message['title'] +" << STATUS Updated >>"
    msg = Message(subject, sender = 'alexxsanya@gmail.com', recipients = [message["email"]])
    msg.body = "Hello {}, Your incident - {} has been updated to {} ".format(message["by_name"],\
                message["comment"],message["status"])
    mail.send(msg) 