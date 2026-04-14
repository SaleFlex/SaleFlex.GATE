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

from .models import Company, UserProfile
from .widgets import (
    AtomicEmailInput,
    AtomicFileInput,
    AtomicPasswordInput,
    AtomicTextarea,
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


COMPANY_REGISTRATION_OPTIONAL_KEYS = (
    "companies_house_number",
    "vat_number",
    "registered_office",
)


def registration_kwargs_from_cleaned(cleaned_data: dict) -> dict[str, str]:
    """Map optional registration fields from a create form's cleaned_data to model kwargs."""
    out: dict[str, str] = {}
    for key in COMPANY_REGISTRATION_OPTIONAL_KEYS:
        raw = cleaned_data.get(key)
        if raw is None:
            out[key] = ""
        elif isinstance(raw, str):
            out[key] = raw.strip()
        else:
            out[key] = str(raw)
    return out


class CompanyCreateForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        label="Company name",
        widget=AtomicTextInput(attrs={"autocomplete": "organization"}),
    )
    companies_house_number = forms.CharField(
        required=False,
        max_length=32,
        label="Companies House number (CRN)",
        help_text="Optional. Company registration number from Companies House.",
        widget=AtomicTextInput(attrs={"autocomplete": "off"}),
    )
    vat_number = forms.CharField(
        required=False,
        max_length=32,
        label="VAT number",
        help_text="Optional. VAT registration number.",
        widget=AtomicTextInput(attrs={"autocomplete": "off"}),
    )
    registered_office = forms.CharField(
        required=False,
        label="Registered office address",
        help_text="Optional. Registered office or principal trading address.",
        widget=AtomicTextarea(attrs={"rows": 3}),
    )

    def clean_name(self) -> str:
        n = (self.cleaned_data.get("name") or "").strip()
        if not n:
            raise forms.ValidationError("Enter a company name.")
        return n


class CompanyRegistrationForm(forms.ModelForm):
    """Owner/admin: edit display name and optional registration fields (slug unchanged)."""

    class Meta:
        model = Company
        fields = ("name",) + COMPANY_REGISTRATION_OPTIONAL_KEYS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget = AtomicTextInput(
            attrs={**self.fields["name"].widget.attrs, "autocomplete": "organization"}
        )
        self.fields["registered_office"].widget = AtomicTextarea(
            attrs={**self.fields["registered_office"].widget.attrs, "rows": 4}
        )
        for key in COMPANY_REGISTRATION_OPTIONAL_KEYS:
            if key == "registered_office":
                continue
            f = self.fields[key]
            f.widget = AtomicTextInput(attrs={**f.widget.attrs, "autocomplete": "off"})

    def clean_name(self) -> str:
        n = (self.cleaned_data.get("name") or "").strip()
        if not n:
            raise forms.ValidationError("Enter a company name.")
        return n

    def clean(self):
        data = super().clean()
        for name, val in list(data.items()):
            if isinstance(val, str):
                data[name] = val.strip()
        return data


class CompanyJoinForm(forms.Form):
    slug = forms.CharField(
        max_length=96,
        label="Company slug",
        help_text="Ask an owner or administrator for the company slug shown on the company page.",
        widget=AtomicTextInput(attrs={"autocomplete": "off"}),
    )
    message = forms.CharField(
        required=False,
        max_length=500,
        label="Message (optional)",
        widget=AtomicTextarea(attrs={"rows": 3}),
    )

    def clean_slug(self) -> str:
        s = (self.cleaned_data.get("slug") or "").strip()
        if not s:
            raise forms.ValidationError("Enter the company slug.")
        return s


class GrantOwnerForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=AtomicTextInput(attrs={"autocomplete": "username"}),
    )

    def clean_username(self) -> str:
        s = (self.cleaned_data.get("username") or "").strip()
        if not s:
            raise forms.ValidationError("Enter a username.")
        return s
