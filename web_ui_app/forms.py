# MIT License
#
# Copyright (c) 2025-2026 Ferhat Mousavi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.contrib.auth.models import User

from .models import UserProfile
from .widgets import (
    AtomicEmailInput,
    AtomicFileInput,
    AtomicPasswordInput,
    AtomicTextInput,
)


class GateAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        u, p = self.fields["username"], self.fields["password"]
        u.widget = AtomicTextInput(attrs={**u.widget.attrs})
        p.widget = AtomicPasswordInput(
            attrs={**p.widget.attrs},
            render_value=p.widget.render_value,
        )


class GatePasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.PasswordInput):
                field.widget = AtomicPasswordInput(
                    attrs={**w.attrs},
                    render_value=w.render_value,
                )


class GateUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Optional. Used for notifications when enabled.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            f = self.fields["username"]
            f.widget = AtomicTextInput(attrs={**f.widget.attrs})
        if "email" in self.fields:
            f = self.fields["email"]
            f.widget = AtomicEmailInput(attrs={**f.widget.attrs})
        for name in ("password1", "password2"):
            if name not in self.fields:
                continue
            f = self.fields[name]
            w = f.widget
            if isinstance(w, forms.PasswordInput):
                f.widget = AtomicPasswordInput(
                    attrs={**w.attrs},
                    render_value=w.render_value,
                )


class GateUserAccountForm(forms.ModelForm):
    """Update signed-in user fields (password is changed elsewhere)."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("first_name", "last_name"):
            if name in self.fields:
                f = self.fields[name]
                f.widget = AtomicTextInput(attrs={**f.widget.attrs})
        if "email" in self.fields:
            f = self.fields["email"]
            f.widget = AtomicEmailInput(attrs={**f.widget.attrs})


class GateUserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("avatar",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields["avatar"]
        f.required = False
        f.label = "Profile picture"
        f.widget = AtomicFileInput(attrs={**f.widget.attrs})
