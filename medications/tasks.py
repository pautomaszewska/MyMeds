from __future__ import absolute_import, unicode_literals
from celery import task
from datetime import date
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Medicine


@task
def email_expired():
    expired = Medicine.objects.filter(expiration_date=date.today())
    for med in expired:
        mail_subject = 'MyMeds - Expired medictions'
        message = render_to_string('expired_mail.html', {'med': med.name})
        recipient = med.user.email
        email = EmailMessage(mail_subject, message, to=[recipient])
        email.send()


