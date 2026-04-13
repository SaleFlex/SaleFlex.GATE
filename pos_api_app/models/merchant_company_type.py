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
