"""Signal handlers for the tracker app."""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserSettings


@receiver(post_save, sender=get_user_model())
def create_user_settings(sender, instance, created, **kwargs):
    """
    Automatically create a UserSettings record for new users.
    """
    if created:
        UserSettings.objects.get_or_create(user=instance)
