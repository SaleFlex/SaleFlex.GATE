from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class GateUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Optional. Used for notifications when enabled.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
