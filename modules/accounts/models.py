from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
import pdb
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django_model_changes import ChangesMixin
from simple_history.models import HistoricalRecords
from django.utils.functional import cached_property


class Users(ChangesMixin, AbstractUser):
	class Meta:
		verbose_name = _('Customer')
		verbose_name_plural = _('  Customers')

	username = models.CharField(_('Username'), max_length=100, unique=True)
	email = models.EmailField(_('Email address'), unique=True)
	first_name = models.CharField(_('First name'), max_length=30, blank=True)
	last_name = models.CharField(_('Last name'), max_length=30, blank=True)
	is_active = models.BooleanField(_('Account active'), default=True)
	is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this portal.'),
    )

	address = models.TextField(_('Address'), null=True, blank=True)
	role = models.ForeignKey(Group, verbose_name=_('Role'), null=True, blank=False, on_delete=models.SET_NULL)
	history = HistoricalRecords()
	created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
	updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ('username',)
	def __str__(self):
		return self.email

	@cached_property
	def account(self):
		return self.bankaccounts

	@cached_property
	def is_customer(self):
		try:
			return self.role.name.lower().startswith('customer')
		except:
			return False



class BankAccounts(models.Model):
	class Meta:
		verbose_name = _(' Account')
		verbose_name_plural = _(' Accounts')

	account_number = models.CharField(_('Account number'), max_length=100, unique=True, validators=[MinLengthValidator(10), MaxLengthValidator(12)])
	customer = models.OneToOneField(Users , on_delete=models.PROTECT, verbose_name=_('Customer'))
	balance = models.FloatField(_('Balance'), default=0)
	history = HistoricalRecords()

	created_at = models.DateTimeField(_('Created At'),auto_now_add=True)
	updated_at = models.DateTimeField(_('Updated At'),auto_now=True)

	def __str__(self):
		return self.account_number

def update_role_permission(sender, instance, **kwargs):
	if instance.changes().get('role'):
		if not instance.changes().get('role')[1] in instance.groups.all():
			instance.groups.remove(instance.changes().get('role')[0])
			instance.groups.add(instance.changes().get('role')[1])
			instance.save()

post_save.connect(update_role_permission, sender=Users)