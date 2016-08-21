from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.db import models
from .models import UpImages

import os

@receiver(models.signals.post_delete, sender=UpImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `UpImages` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
