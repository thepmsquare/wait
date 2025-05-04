from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


from django import forms
from .models import WeightEntry


class WeightEntryForm(forms.ModelForm):
    """
    Form for creating and updating WeightEntry instances.
    """

    class Meta:
        """
        Meta options for the WeightEntryForm.
        """

        model = WeightEntry
        fields = ["weight", "timestamp"]
        widgets = {
            "timestamp": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
