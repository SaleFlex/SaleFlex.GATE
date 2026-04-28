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


class PosPaymentType(models.Model):
    # Type number (required)
    type_no = models.IntegerField()

    # Name of the payment type (required)
    name = models.CharField(max_length=255)

    # Culture information (e.g., en-US, fr-FR) (required)
    culture_info = models.CharField(max_length=50)

    # Optional description of the payment type
    type_description = models.TextField(blank=True, null=True)

    # Foreign key to POS, allows the payment type to be related to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_types')

    # Foreign key to Store, allows the payment type to be sent to all POS devices in a store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_types')

    # Foreign key to Merchant, allows the payment type to be sent to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='payment_types')

    # Indicates if the pos payment type has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False)

    # Optional description or reason for deletion
    delete_description = models.CharField(max_length=255, blank=True, null=True)

    # User information: who created the POS payment type
    created_by = models.ForeignKey(User, related_name='pos_payment_type_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the POS payment type is created
    created_at = models.DateTimeField(auto_now_add=True)

    # User information: who last updated the POS payment type
    updated_by = models.ForeignKey(User, related_name='pos_payment_type_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the POS payment type is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Adding constraints for unique combination of type_no and culture_info to match SQL UNIQUE constraint
        constraints = [
            models.UniqueConstraint(fields=['type_no', 'culture_info'], name='unique_type_no_culture_info')
        ]

    def __str__(self):
        return f"{self.type_name} ({self.type_no})"
