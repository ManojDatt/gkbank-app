from django import template
register = template.Library()
from ..models import Users
from modules.bankings.models import Transactions

@register.simple_tag
def news():
	return []

@register.simple_tag
def transactions():
	return Transactions.objects.count()

@register.simple_tag
def customers():
	return Users.objects.count()