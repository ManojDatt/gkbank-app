from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
#from conf import celeryconfig

#set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE','GkBank.settings')
app = Celery('GkBank')

#Using a string here means the worker will not have to
#pickle the object when using Windows.
app.config_from_object('django.conf:settings')
#app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@app.task(name="Send Transaction Mail TO Customer")
def send_transaction_mail(trans_type, json_data, email):
	subject = f'Your transaction for {trans_type} processed.'
	html_message = render_to_string('transaction_mail.html',json_data)
	plain_message = strip_tags(html_message)
	send_mail(subject, plain_message, 'support@gkmit.com', [email], fail_silently=False)
