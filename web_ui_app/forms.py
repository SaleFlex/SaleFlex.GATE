# SaleFlex.GATE - Point of Sale Application Gateway
# Copyright (C) 2025-2026 Mousavi.Tech
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

from typing import Iterable

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.db.models import Q

from core.models import Cashier, Company, Country, CountryTemplate
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


class CashierCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Optional. Used for notifications when enabled.")

    class Meta(UserCreationForm.Meta):
        model = Cashier
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


class CashierAccountForm(forms.ModelForm):
    """Update signed-in cashier fields (password is changed elsewhere)."""

    class Meta:
        model = Cashier
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


class CashierAvatarForm(forms.ModelForm):
    class Meta:
        model = Cashier
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

PORTAL_SESSION_COUNTRY_PK = "portal_company_create_country_pk"
WIZARD_STEP_COUNTRY = "country"
WIZARD_STEP_DETAILS = "details"

DEFAULT_REGISTRATION_DEFS: tuple[dict, ...] = (
    {
        "key": "companies_house_number",
        "label": "Companies House number (CRN)",
        "help_text": "Optional. Company registration number from Companies House.",
        "widget": "text",
        "textarea_rows": 3,
    },
    {
        "key": "vat_number",
        "label": "VAT number",
        "help_text": "Optional. VAT registration number.",
        "widget": "text",
        "textarea_rows": 3,
    },
    {
        "key": "registered_office",
        "label": "Registered office address",
        "help_text": "Optional. Registered office or principal trading address.",
        "widget": "textarea",
        "textarea_rows": 3,
    },
)


def portal_active_countries():
    """Countries eligible for onboarding (respects soft-delete when used)."""

    return (
        Country.objects.filter(Q(is_deleted=False) | Q(is_deleted__isnull=True)).order_by("name")
    )


def active_template_for_country_id(country_id: int | None) -> CountryTemplate | None:
    if not country_id:
        return None
    return CountryTemplate.objects.filter(country_id=country_id, is_active=True).first()


def active_template_for_country(country: Country | None) -> CountryTemplate | None:
    if not country or not country.pk:
        return None
    return active_template_for_country_id(int(country.pk))


def merged_registration_defs(template: CountryTemplate | None) -> list[dict]:
    rows: list[dict] = [dict(row) for row in DEFAULT_REGISTRATION_DEFS]
    if not template or not template.registration_field_defs:
        return rows
    if not isinstance(template.registration_field_defs, list):
        return rows
    overrides = {item["key"]: item for item in template.registration_field_defs if isinstance(item, dict)}
    for i, row in enumerate(rows):
        key = row["key"]
        override = overrides.get(key)
        if not override:
            continue
        if override.get("label"):
            rows[i]["label"] = override["label"]
        if "help_text" in override:
            rows[i]["help_text"] = override["help_text"]
        elif override.get("help") is not None:
            rows[i]["help_text"] = override["help"]
        if override.get("widget") in {"text", "textarea"}:
            rows[i]["widget"] = override["widget"]
        if override.get("textarea_rows"):
            rows[i]["textarea_rows"] = int(override["textarea_rows"])
    return rows


def apply_optional_registration_defs(form: forms.BaseForm, defs: Iterable[dict]) -> None:
    """Apply label/help/widget hints for COMPANY_REGISTRATION_OPTIONAL_KEYS fields."""

    for row in defs:
        key = row.get("key")
        if not key or key not in form.fields:
            continue
        field = form.fields[key]
        label = row.get("label")
        if label:
            field.label = label
        if "help_text" in row and row["help_text"] is not None:
            field.help_text = row["help_text"]
        widget = row.get("widget") or "text"
        rows = int(row.get("textarea_rows") or 3)
        if widget == "textarea":
            field.widget = AtomicTextarea(attrs={**field.widget.attrs, "rows": rows})
        else:
            field.widget = AtomicTextInput(attrs={**field.widget.attrs, "autocomplete": "off"})


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


class CompanyWizardCountryStepForm(forms.Form):
    wizard_step = forms.CharField(initial=WIZARD_STEP_COUNTRY, widget=forms.HiddenInput)
    country = forms.ModelChoiceField(
        queryset=Country.objects.none(),
        label="Country",
        empty_label=None,
    )

    def __init__(
        self,
        *args,
        countries_queryset=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        qs = portal_active_countries() if countries_queryset is None else countries_queryset
        self.fields["country"].queryset = qs


class CompanyCreateForm(forms.Form):
    wizard_step = forms.CharField(required=False, initial=WIZARD_STEP_DETAILS, widget=forms.HiddenInput)

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

    def __init__(self, *args, is_wizard: bool = False, registration_defs: list[dict] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        if not is_wizard:
            self.fields.pop("wizard_step", None)
        defs = registration_defs if registration_defs is not None else merged_registration_defs(None)
        apply_optional_registration_defs(self, defs)

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
        tpl = active_template_for_country(getattr(self.instance, "country", None))
        defs = merged_registration_defs(tpl)
        apply_optional_registration_defs(self, defs)
        ro_widget = self.fields["registered_office"].widget
        if isinstance(ro_widget, AtomicTextarea):
            prev = int(ro_widget.attrs.get("rows") or 4)
            ro_widget.attrs["rows"] = max(prev, 4)
        for key in COMPANY_REGISTRATION_OPTIONAL_KEYS:
            if key == "registered_office":
                continue
            self.fields[key].widget = AtomicTextInput(
                attrs={**self.fields[key].widget.attrs, "autocomplete": "off"}
            )

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
