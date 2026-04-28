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
from django.contrib.auth.models import User


# No: 1
# Name: United States Dollars
# RateOfCurrency: 220 means 2.20
# CurrencyCode: 840
# Sign: $
# SignDirection: R
# CurrencySymbol: USD
class PosCurrency(models.Model):
    # Currency number (unique for each currency)
    no = models.IntegerField()

    # Name of the currency (e.g., United States Dollar)
    name = models.CharField(max_length=255)

    # Currency rate (e.g., exchange rate)
    rate_of_currency = models.IntegerField()

    # ISO currency code (e.g., 840 for USD)
    currency_code = models.IntegerField()

    # Currency sign (e.g., $)
    sign = models.CharField(max_length=10)

    # Sign direction (e.g., 'R' for right, 'L' for left)
    sign_direction = models.CharField(max_length=1)

    # Currency symbol (e.g., USD)
    currency_symbol = models.CharField(max_length=10)

    # Foreign key to POS, optional, allows the form to be related to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='currencies')

    # Foreign key to Store, optional, allows the form to be sent to all POS devices in a store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='currencies')

    # Foreign key to Merchant, optional, allows the form to be sent to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='currencies')

    # A field to track if the currency is currently active
    is_active = models.BooleanField(default=True)

    # Optional effective date for when the currency rate becomes applicable
    effective_date = models.DateTimeField(null=True, blank=True)

    # Optional expiration date for when the currency rate is no longer valid
    expiration_date = models.DateTimeField(null=True, blank=True)

    # Indicates if the currency entry has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for deletion (if applicable)
    delete_description = models.CharField(max_length=255)

    # Foreign key to the User model, represents the user who created this currency entry
    created_by = models.ForeignKey(User, related_name='currency_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the currency entry is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this currency entry
    updated_by = models.ForeignKey(User, related_name='currency_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the currency entry is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['no', 'pos', 'merchant', 'store'], name='unique_currency_for_merchant_store')
        ]

    def __str__(self):
        return f"Currency {self.name} - {self.currency_symbol} ({self.no})"
