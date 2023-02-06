from os import getenv
from app import mail
from flask_mail import Message
from flask import render_template


class Mailing:
    def __init__(self):
        self.sender = ('Flask Boilerplate', getenv('MAIL_USERNAME'))

    def emailResetPassword(self, recipient, name, password):
        html = render_template(
            'reset_password.html',
            name=name,
            password=password
        )
        return self.__sendEmail(
            f'Reseteo de Contraseña - {name}',
            [recipient],
            html
        )

    def __sendEmail(self, subject, recipients, body):
        message = Message(
            subject=subject,
            sender=self.sender,
            recipients=recipients,
            html=body
        )
        return mail.send(message)
