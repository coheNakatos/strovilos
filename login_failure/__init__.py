""" 
A reusable app that logs failed logins
including the remote IP address.From there
fail2ban takes action.
"""
from django.contrib.auth.signals import user_login_failed

from login_failure.signals import get_request

import logging

logger = logging.getLogger('fail2ban')

def log_login_failure(sender, credentials, **kwargs):
    http_request = get_request()

    msg = "Login failure {}".format(http_request.META.get('HTTP_X_FORWARDED_FOR'))
    logger.error(msg)

user_login_failed.connect(log_login_failure)