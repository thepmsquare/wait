from decimal import Decimal

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
    Handles dynamic conversion of target_weight to/from kg based on
    preferred_unit.
    """

    class Meta:
        model = UserSettings
        fields = ["target_weight", "preferred_unit"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.preferred_unit == "lb":
                # Convert target_weight in kg to lb for display
                lb_val = Decimal(self.instance.target_weight) / Decimal("0.45359237")
                self.initial["target_weight"] = round(lb_val, 2)

    def save(self, commit=True):
        instance = super().save(commit=False)
        target_weight = self.cleaned_data.get("target_weight")
        preferred_unit = self.cleaned_data.get("preferred_unit")
        if preferred_unit == "lb":
            # Convert target_weight in lb to kg for DB storage
            instance.target_weight = round(target_weight * Decimal("0.45359237"), 2)
        else:
            instance.target_weight = target_weight
        if commit:
            instance.save()
        return instance
