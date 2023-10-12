from flask_mail import Message,Mail

from run import app
from app import mail



def send_email(to, subject, template):
    mail = Mail(app)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)

