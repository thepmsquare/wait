from django import forms
from django.utils import timezone

from .models import UserSettings, WeightEntry


class LowercaseFormMixin:
    """
    Mixin to dynamically convert all form field labels and help texts to
    lowercase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label:
                field.label = field.label.lower()
            if field.help_text:
                field.help_text = field.help_text.lower()


class WeightEntryForm(LowercaseFormMixin, forms.ModelForm):
    """
    Form for creating and updating WeightEntry instances.
    """

    class Meta:
        """
        Meta options for the WeightEntryForm.
        """

        model = WeightEntry
        fields = ["weight", "unit", "timestamp"]
        widgets = {
            "timestamp": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_timestamp(self):
        timestamp = self.cleaned_data["timestamp"]
        if timestamp > timezone.now():
            raise forms.ValidationError("timestamp cannot be in the future.")
        return timestamp


class UserSettingsForm(LowercaseFormMixin, forms.ModelForm):
    """
    Form for updating UserSettings.
    """

    class Meta:
        model = UserSettings
        fields = ["preferred_unit"]
