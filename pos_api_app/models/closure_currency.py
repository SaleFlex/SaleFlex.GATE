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

from django.db import models
from django.contrib.auth.models import User


class ClosureCurrency(models.Model):
    # Links this closure currency to a specific closure event
    closure = models.ForeignKey('Closure', on_delete=models.CASCADE)

    # The currency used for transactions during this closure (ForeignKey to PosCurrency)
    currency = models.ForeignKey('PosCurrency', on_delete=models.CASCADE)

    # Exchange rate for the currency at the time of closure
    rate_of_currency = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)

    # The number of transactions or entries in this currency
    currency_count = models.IntegerField()

    # Total transaction amount in the foreign currency
    currency_foreign_total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Total transaction amount in the domestic currency (after conversion)
    currency_domestic_total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Flag to indicate if this is the base currency of the store or POS system
    is_base_currency = models.BooleanField(default=False)

    # Soft delete flag to indicate if this record has been marked as deleted
    is_deleted = models.BooleanField(default=False, null=True)

    # Reason or description for deletion (if applicable)
    delete_description = models.CharField(max_length=255, null=True, blank=True)

    # Tracks the user who created the record
    created_by = models.ForeignKey(User, related_name='closure_currency_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Tracks the user who last updated the record
    updated_by = models.ForeignKey(User, related_name='closure_currency_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically stores the timestamp when the record was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically stores the timestamp when the record was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Currency {self.currency.name} - Foreign: {self.currency_foreign_total_amount}, Domestic: {self.currency_domestic_total_amount}"
