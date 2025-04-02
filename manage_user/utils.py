import random
from .models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from lebricoleur.celery import app


@app.task
def send_normal_email(data):
    email =EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]

    )
    email.send()

