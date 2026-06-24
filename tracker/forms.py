from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import WeightEntry


class LowercaseFormMixin:
    """
    Mixin to dynamically convert all form field labels and help texts to lowercase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.label:
                field.label = field.label.lower()
            if field.help_text:
                field.help_text = field.help_text.lower()


class CustomUserCreationForm(LowercaseFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)


class CustomAuthenticationForm(LowercaseFormMixin, AuthenticationForm):
    pass


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
