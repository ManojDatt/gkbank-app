from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django_model_changes import ChangesMixin
from simple_history.models import HistoricalRecords
from django.utils.functional import cached_property
import random
import string, pdb
from modules.accounts.models import Users

def trans_generator():
	size = 10
	chars = string.ascii_lowercase + string.digits
	code = ''.join(random.choice(chars) for _ in range(size))
	while Transactions.objects.filter(translation=code).exists():
		code = ''.join(random.choice(chars) for _ in range(size))
	return code

class Transactions(ChangesMixin, models.Model):
	TRANS_TYPE = (
		('Deposit', _('Deposit')),
		('Withdraw', _('Withdraw')),)
	class Meta:
		verbose_name = _('Transaction')
		verbose_name_plural = _('  Transactions')

	label = models.CharField(_('Label'), max_length=150)
	translation = models.CharField(_('Transaction id'), max_length=100, unique=True, default=trans_generator)
	trans_type = models.CharField(_('Transaction type'), max_length=30, choices=TRANS_TYPE)
	amount = models.FloatField(_('Amount'), default=0)
	status = models.BooleanField(_('Transaction status'), default=True)
	customer = models.ForeignKey(Users, verbose_name=_('Customer'), on_delete=models.PROTECT)
	history = HistoricalRecords()
	created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

	def __str__(self):
		return self.translation


class TransactionReport(models.Model):
	class Meta:
		verbose_name = _('Report')
		verbose_name_plural = _('  Reports')

	translation = models.ForeignKey(Transactions, verbose_name=_('Customer'), on_delete=models.CASCADE)
	amount_total = models.FloatField(_('Amount total'), default=0)
	amount_deposit = models.FloatField(_('Amount deposit'), default=0)
	amount_withdraw = models.FloatField(_('Amount withdraw'), default=0)
	created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

	def __str__(self):
		return str(self.translation.translation)

	@cached_property
	def trans_type(self):
		return self.translation.trans_type

	@cached_property
	def ac_number(self):
		try:
			return self.translation.customer.account.account_number
		except:
			return ""

	@cached_property
	def label(self):
		return self.translation.label


def reset_balance(sender, instance, created, *args,**kwargs):
	current_account = instance.customer.account
	if instance.trans_type == 'Deposit':
		amount_total = current_account.balance + instance.amount
		obj = TransactionReport(translation=instance, amount_total=amount_total, amount_deposit=instance.amount)
		obj.save()
		current_account.balance = amount_total
		current_account.save()
	elif instance.trans_type == 'Withdraw':
		amount_total = current_account.balance - instance.amount
		obj = TransactionReport(translation=instance, amount_total=amount_total, amount_withdraw=instance.amount)
		obj.save()
		current_account.balance = amount_total
		current_account.save()
	# try:
	import pdb
	pdb.set_trace()
	from GkBank.celery import send_transaction_mail
	from datetime import datetime
	context = {'label': instance.label,
				'username': instance.customer.username,
				'amount_total': amount_total,
				'trans_amount': instance.amount,
				'trans_type': instance.trans_type,
				'date': datetime.now()}
	send_transaction_mail.delay(instance.trans_type, context ,instance.customer.email)
	# except:
		# pass

post_save.connect(reset_balance, sender=Transactions)