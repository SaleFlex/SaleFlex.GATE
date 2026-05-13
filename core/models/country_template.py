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

"""Static per-country operational defaults (VAT bands, currencies, languages) for GATE."""

from django.db import models

from .base import BaseModel
from .country import Country


class CountryTemplate(BaseModel):
    """
    Staff-managed template row for one Country: fiscal defaults and UI copy for onboarding.

    `vat_rates` example:
        [{"code": "standard", "label": "Standard VAT", "rate_percent": "20.00"}]

    `registration_field_defs` example (keys map to optional Company registration columns):
        [
          {"key": "companies_house_number", "label": "CRN", "help": "…", "widget": "text"},
          {"key": "vat_number", "label": "VAT number", "help": "…", "widget": "text"},
          {"key": "registered_office", "label": "Address", "help": "…", "widget": "textarea"}
        ]
    """

    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name="template",
        help_text="One template row per country record.",
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Inactive templates are ignored by the portal wizard.",
    )

    default_currency_code = models.CharField(
        max_length=3,
        blank=True,
        help_text="ISO 4217 code used as the primary trading currency hint (e.g. GBP).",
    )
    secondary_currency_codes = models.JSONField(
        null=True,
        blank=True,
        help_text='Optional ISO 4217 list, e.g. ["EUR", "USD"].',
    )

    vat_rates = models.JSONField(
        null=True,
        blank=True,
        help_text='List of {code, label, rate_percent} defaults for VAT / sales tax.',
    )

    language_tags = models.JSONField(
        null=True,
        blank=True,
        help_text='BCP 47 language tags supported for this jurisdiction, e.g. ["en-GB"].',
    )
    default_language_tag = models.CharField(
        max_length=24,
        blank=True,
        help_text="Suggested default UI locale for this template (BCP 47).",
    )

    measurement_unit_system = models.CharField(
        max_length=16,
        blank=True,
        help_text='Optional hint: "metric", "imperial", or free text.',
    )

    wizard_intro = models.TextField(
        blank=True,
        help_text="Optional paragraph shown on the company details step of the wizard.",
    )
    registration_field_defs = models.JSONField(
        null=True,
        blank=True,
        help_text="Optional overrides for portal labels/help on optional Company.registration_* fields.",
    )

    notes = models.TextField(blank=True, help_text="Internal admin notes.")

    class Meta:
        db_table = "CountryTemplate"

    def __str__(self) -> str:
        cn = getattr(self.country, "name", "") or ""
        return f"{cn} — operational template" if cn else f"CountryTemplate ({self.country_id})"

