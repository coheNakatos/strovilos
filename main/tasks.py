from huey import RedisHuey
from huey.contrib.djhuey import crontab, periodic_task, task
from django.core.cache import cache as redis_cache
from django.conf import settings
from .models import Posts
from django.db import transaction, IntegrityError
import logging
logger = logging.getLogger('huey.consumer')

# This is necessary in order to get the right RedisHuey instance.
huey = RedisHuey('main', password = 'zWm$8j3;%_0b8y^^%8xA5EOVWy2B')

@huey.periodic_task(crontab(minute='*/1'))
def viewcountupdate():
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
						post = Posts.objects.get(id=post_id)
						old_viewcount = post.viewcount
						post.viewcount = post.viewcount + hourly_viewcount
						new_viewcount = post.viewcount
						logger.info('Updated: id = {0}. Oldcount = {1} -> Newcount = {2} '.format(post_id, old_viewcount, new_viewcount))
						post.save(update_fields=['viewcount'])
			except IntegrityError:
				transaction.rollback()
			redis_cache.delete_pattern(PREFIX + "*")
	logger.info('Exiting viewcountupdate...')


@huey.task()
def increasecnt(post_id):
	# A lock is being used to make this "process" thread-safe
	PREFIX = settings.CACHE_PREFIX
	endkey = prefixing(PREFIX, post_id)
	with redis_cache.lock('lock'):
		if redis_cache.get(endkey):
			redis_cache.incr(endkey)
		else:
			# Timeout is set to infinite (None)
			redis_cache.set(endkey, 1, timeout=None)
		logger.info("New View Count For id = {0} is {1} with TTL = {2}".format(post_id, redis_cache.get(endkey), redis_cache.ttl(endkey)))

def prefixing(prefix, post_id):
	return prefix + str(post_id)	
