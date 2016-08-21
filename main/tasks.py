from django.core.cache import cache as redis_cache
from django.core.mail import EmailMultiAlternatives
from django.db import transaction, IntegrityError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import Posts

from huey.contrib.djhuey import crontab
from huey import RedisHuey
import logging

logger = logging.getLogger('huey.consumer')

# This is necessary in order to get the right RedisHuey instance.
huey = RedisHuey('main', password = settings.CACHE_PASSWORD)

@huey.periodic_task(crontab(minute='0', hour='*/1'))
def viewcountupdate():
	""" This task is being executed hourly
	and pushed the cached view counters
	into the database using a single transaction
	"""

	# This is the prefix we are going to use to distinguish the cache keys
	# we need for the view counters
	PREFIX = settings.CACHE_PREFIX
	logger.info('Entering viewcountupdate...')
	with redis_cache.lock('lock'):
		keys = redis_cache.keys(PREFIX + "*")
		if keys:
			try:
				with transaction.atomic():
					for key in keys:
						post_id = key.split('_')[1]
						hourly_viewcount = redis_cache.get(key)
						try:
							post = Posts.objects.get(id=post_id)
						except ObjectDoesNotExist:
							continue;
						old_viewcount = post.viewcount
						post.viewcount = post.viewcount + hourly_viewcount
						new_viewcount = post.viewcount
						logger.warn('Updated: id = {0}. Oldcount = {1} -> Newcount = {2} '.format(post_id, old_viewcount, new_viewcount))
						post.save(update_fields=['viewcount'])
			except IntegrityError:
				transaction.rollback()
			redis_cache.delete_pattern(PREFIX + "*")
	logger.info('Exiting viewcountupdate...')


@huey.task()
def increasecnt(post_id):
	""" This is being called on each article request
	and asynchronously increases a view counter by 1 
	"""
	# A lock is being used to make this "process" thread-safe
	PREFIX = settings.CACHE_PREFIX
	endkey = prefixing(PREFIX, post_id)
	with redis_cache.lock('lock'):
		if redis_cache.get(endkey):
			redis_cache.incr(endkey)
		else:
			# Timeout is set to infinite (None)
			redis_cache.set(endkey, 1, timeout=5400)
		logger.warn("New View Count For id = {0} is {1} with TTL = {2}".format(post_id, redis_cache.get(endkey), redis_cache.ttl(endkey)))

def prefixing(prefix, post_id):
	return prefix + str(post_id)

@huey.task()
def async_mail(form):
	""" An async task to send the email
	submited through the index's form
	"""
	name = form.cleaned_data['name']
	email_addr = form.cleaned_data['email']
	message = form.cleaned_data['message']
	subject = form.cleaned_data['subject']
	email = EmailMultiAlternatives(
		subject = subject,
		body = message,
		from_email = name + "<" + settings.DEFAULT_FROM_EMAIL + ">",
		to = [settings.DEFAULT_TO_EMAIL],
		headers = {"Reply-To" : email_addr}
		)
	logger.warn("Subject: {0}".format(subject))
	logger.warn("From: {0} -> Reply-To: {1}".format(name, email_addr))
	logger.warn("Body: {0}".format(message))
	logger.warn(email.send())
