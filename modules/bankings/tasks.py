from celery.decorators import task

@task(name="Send Transaction Mail TO Customer")
def send_transaction_mail(trans_type, json_data):
    print('Request: {0!r}'.format(trans_type))