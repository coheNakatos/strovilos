from __future__ import absolute_import
from celery.task import periodic_task
from celery.schedules import crontab
from celery import shared_task, task
from django.core.cache import cache
import logging

logger = logging.getLogger('main')

@shared_task
@periodic_task(
	name='viewcountupdate',
	run_every=crontab(minute='*/5'))
def viewcountupdate():
	#TODO: implement push to database
	logger.debug('Updating Posts\' counts')

@shared_task
@task(name='increacecnt')
def increasecnt(post_id):

	# We use _client attribute, which is the memcached client instance
	# so that we can access the atomic operation incr()
	memcached_client = cache._client
	
	# memcached client requires strings as inputs to its functions 
	post_id = str(post_id)
	
	if memcached_client.get(post_id):
		memcached_client.incr(post_id)
	else:
		memcached_client.set(post_id, 1)
	# This is not thread safe, but the incr() function is still atomic
	logger.debug("New value for {0} is {1}".format(post_id, memcached_client.get(post_id)))
	

