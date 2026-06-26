"""
models for the tracker app.
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class WeightEntry(models.Model):
    """
    model to store a user's weight at a specific point in time.
    """

    objects = models.Manager()

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="weight_entries",
    )
    class UnitChoices(models.TextChoices):
        KG = "kg", "kg"
        LB = "lb", "lb"

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="enter your weight",
    )
    unit = models.CharField(
        max_length=2,
        choices=UnitChoices.choices,
        default=UnitChoices.KG,
        help_text="unit of the weight measurement (kg or lb)",
    )

    timestamp = models.DateTimeField(
        default=timezone.now, help_text="date and time of the weight measurement."
    )

    class Meta:
        """
        Meta options for the WeightEntry model.
        """

        ordering = ["-timestamp"]
        verbose_name = "weight entry"
        verbose_name_plural = "weight entries"

    def __str__(self):
        """
        String representation of the WeightEntry object.
        """
        return f"{self.weight} {self.unit} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class UserSettings(models.Model):
    """
    model to store user preferences like target weight and preferred display unit.
    """

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="settings",
    )
    target_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=75.00,
        help_text="enter your target weight in kg",
    )
    preferred_unit = models.CharField(
        max_length=2,
        choices=WeightEntry.UnitChoices.choices,
        default=WeightEntry.UnitChoices.KG,
        help_text="preferred display unit",
    )

    class Meta:
        verbose_name = "user settings"
        verbose_name_plural = "user settings"

    def __str__(self):
        return f"{self.user.username}'s settings"


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=get_user_model())
def create_user_settings(sender, instance, created, **kwargs):
    """
    Automatically create a UserSettings record for new users.
    """
    if created:
        UserSettings.objects.get_or_create(user=instance)

