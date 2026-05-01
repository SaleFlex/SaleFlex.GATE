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

from django.db import models


class Company(models.Model):
    """Portal tenant (hub company). Distinct from pos_api_app.Merchant until linked."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=96, unique=True, db_index=True)
    # Optional registration details (aligned with typical UK limited-company data; only name is required)
    companies_house_number = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="Companies House number",
        help_text="Company registration number (CRN) from Companies House, if applicable.",
    )
    vat_number = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="VAT number",
        help_text="VAT registration number, if applicable.",
    )
    registered_office = models.TextField(
        blank=True,
        verbose_name="Registered office address",
        help_text="Registered office or principal trading address, if recorded.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def has_registration_details(self) -> bool:
        return bool(
            self.companies_house_number
            or self.vat_number
            or self.registered_office
        )
