from .models import UpImages, BodyText, Category
from django.core.cache import cache as redis_cache

def get_base_context(form_errors=None):
	"""
	This is used to obtain the basic, shared by all views, context.
	In-Memory cache is being used to quickly access this context.
	"""
	logo = redis_cache.get('logo')
	if not logo:
		logo = UpImages.objects.get(image_title="Logo")
		redis_cache.set('logo', logo)	
	quote = redis_cache.get('quote')		
	if not quote:
		quote = BodyText.objects.get(description='Γνωμικό')
		redis_cache.set('quote', quote)
	categories = redis_cache.get('categories')
	if not categories:
		categories = Category.objects.all()
		redis_cache.set('categories', categories)
	context = {'logo': logo, 'quote': quote, 'categories': categories}
	if form_errors:
		context['form_errors']=form_errors
	return context