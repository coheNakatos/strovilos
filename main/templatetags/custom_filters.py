from django.template.defaultfilters import truncatewords, safe
from django import template

register = template.Library()

@register.filter
def trunc(value, arg):
	return truncatewords(safe(value), arg) 
