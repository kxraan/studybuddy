from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_group_email(subject, recipients, body):
    try:
        msg = Message(
            subject,
            recipients=recipients,
            body=body,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error sending email: {e}")