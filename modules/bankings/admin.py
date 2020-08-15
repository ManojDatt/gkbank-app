from django.contrib import admin
from .models import Transactions, TransactionReport
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from simple_history.models import HistoricalRecords
from django.db.models import Sum, Q
from django import forms
import pdb
from django.core.exceptions import ValidationError

class TransactionsForm(forms.ModelForm):
	class Meta:
		model = Transactions
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(TransactionsForm, self).__init__(*args, **kwargs)
		from modules.accounts.models import Users
		if self.fields.get('customer', False):
			if self.current_user.is_customer:
				self.fields['customer'].queryset = Users.objects.filter(id=self.current_user.id)
				self.fields['customer'].initial = self.current_user
				self.fields['customer'].widget.attrs['readonly'] = True
			else:
				self.fields['customer'].queryset = Users.objects.exclude(id=self.current_user.id)


	def clean(self):
		cleaned_data = super(TransactionsForm, self).clean()
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			if instance.trans_type == 'Withdraw' and instance.amount > instance.customer.account.balance:
				raise ValidationError(f"Available amount {instance.customer.account.balance} only.")
		else:
			if cleaned_data['amount'] > cleaned_data['customer'].account.balance:
				raise ValidationError(f"Available amount {instance.customer.account.balance} only.")


@admin.register(Transactions)
class TransactionsAdmin(SimpleHistoryAdmin):
	"""
	All Transactions
	"""
	form = TransactionsForm
	list_display = ('label', 'translation','trans_type', 'amount',  'customer','updated_at',)
	list_filter = ('trans_type', 'status',)

	def has_add_permission(self, request):
		if request.user.is_customer:
			return True
		return super().has_add_permission(request)

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def get_form(self, request, *args, **kwargs):
		form = super(TransactionsAdmin, self).get_form(request, *args, **kwargs)
		form.current_user = request.user
		return form