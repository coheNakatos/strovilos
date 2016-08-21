from login_failure.signals import request_accessor


class RequestProviderError(Exception):
    pass


class RequestProvider(object):
    """
    This middleware listens for signals sent when
    user_failed_login signal is triggered. Then sends
    back the request object.
    """
    def __init__(self):
        self._request = None
        request_accessor.connect(self)

    def process_request(self, request):
        self._request = request
        return None

    def __call__(self, **kwargs):
        return self._request