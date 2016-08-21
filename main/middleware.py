from django.conf import settings
from django.utils import translation


class AdminLocaleURLMiddleware:
	""" A middleware to override the LANGUAGE_CODE
	and set it according to settings.ADMIN_LANGUAGE_CODE
	"""
	def process_request(self, request):
		if request.path.startswith('/admin'):
			request.LANG = getattr(settings, 'ADMIN_LANGUAGE_CODE', settings.LANGUAGE_CODE)
			translation.activate(request.LANG)
			request.LANGUAGE_CODE = request.LANG