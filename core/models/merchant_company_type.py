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

from django.contrib.auth.models import User
from django.db import models


class MerchantCompanyType(models.Model):
    # Name of the company type, e.g., "Limited Company", "Incorporated"
    name = models.CharField(max_length=100, unique=True)

    # Short code for the company type, e.g., "LTD", "INC", "LLC"
    code = models.CharField(max_length=10, unique=True)

    # Optional description to explain the company type
    description = models.TextField(null=True, blank=True)

    # Indicates if the company type has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Foreign key to the User model, represents the user who created this country record
    created_by = models.ForeignKey(User, related_name='merchant_company_type_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the country record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this country record
    updated_by = models.ForeignKey(User, related_name='merchant_company_type_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the country record is updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        db_table = 'MerchantCompanyType'
        verbose_name = 'Merchant Company Type'
        verbose_name_plural = 'Merchant Company Types'
