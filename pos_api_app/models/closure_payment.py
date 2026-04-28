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


class ClosurePayment(models.Model):
    # Links this closure payment type to a specific closure event
    closure = models.ForeignKey('Closure', on_delete=models.CASCADE)

    # Payment type associated with this closure
    payment_type = models.ForeignKey('PosPaymentType', on_delete=models.CASCADE)

    # The number of transactions or entries in this payment type
    payment_type_count = models.IntegerField()

    # Total transaction amount in the payment type
    payment_type_total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Soft delete flag to indicate if this record has been marked as deleted
    is_deleted = models.BooleanField(default=False, null=True)

    # Reason or description for deletion (if applicable)
    delete_description = models.CharField(max_length=255, null=True, blank=True)

    # Tracks the user who created the record
    created_by = models.ForeignKey(User, related_name='closure_payment_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Tracks the user who last updated the record
    updated_by = models.ForeignKey(User, related_name='closure_payment_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically stores the timestamp when the record was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically stores the timestamp when the record was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.payment_type.name} - Total Amount: {self.payment_type_total_amount}"
