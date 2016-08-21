from django.conf import settings

def global_settings(request):
	"""Add here any settings fields
	you need in templates.
	"""
	return {
		'TITLE_COUNT': settings.TITLE_COUNT,
		'DESC_COUNT': settings.DESC_COUNT,
	}
