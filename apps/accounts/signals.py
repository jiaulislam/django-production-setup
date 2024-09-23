from logging import getLogger

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile

_logger = getLogger(__name__)

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created: bool, **kwargs):
    if created:
        _logger.debug("creating profile for %r", instance)
        UserProfile.objects.create(user=instance)
