from django.dispatch import Signal

class UnauthorizedSignalReceiver(Exception):
    pass

class SingleHandlerSignal(Signal):

    allowed_receiver = 'login_failure.middleware.RequestProvider'

    def __init__(self, providing_args=None):
        return Signal.__init__(self, providing_args)

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
        receiver_name = '.'.join([receiver.__class__.__module__,
                                   receiver.__class__.__name__ ])

        if receiver_name != self.allowed_receiver:
            raise UnauthorizedSignalReceiver()

        Signal.connect(self, receiver, sender, weak, dispatch_uid)

request_accessor = SingleHandlerSignal()

def get_request():
    """ Sender=None, sent to all receivers
    so [0] indicates the response of the first receiver,
    in our case the middleware that sends us back the 
    request object.Responses are sent back as a tuple of
    (receiver,response), so [1] indicates the response
    of this particular receiver.
    """
    return request_accessor.send(None)[0][1]