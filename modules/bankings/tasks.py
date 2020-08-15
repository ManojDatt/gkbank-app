from celery.decorators import task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@task(name="Send Transaction Mail TO Customer")
def send_transaction_mail(trans_type, json_data, email):
	subject = f'Your transaction for {trans_type} processed.'
	html_message = render_to_string('transaction_mail.html',json_data)
	plain_message = strip_tags(html_message)
	from_email = 'From <from@example.com>'
	send_mail(subject, plain_message, 'support@gkmit.com', [email], fail_silently=False)
