# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class WeightEntry(models.Model):
    """
    Model to store a user's weight at a specific point in time.
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="weight_entries",
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Enter your weight in kilograms",
    )

    timestamp = models.DateTimeField(
        default=timezone.now, help_text="Date and time of the weight measurement."
    )

    class Meta:
        """
        Meta options for the WeightEntry model.
        """

        ordering = ["-timestamp"]
        verbose_name = "Weight Entry"
        verbose_name_plural = "Weight Entries"

    def __str__(self):
        """
        String representation of the WeightEntry object.
        """
        return f"{self.weight} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
