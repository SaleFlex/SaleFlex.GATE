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


class WarehouseTransaction(models.Model):
    # Warehouse Id (ForeignKey to a Warehouse model)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='transactions')

    # Product Id (ForeignKey to a Product model)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='transactions')

    # Transaction Type (Entry, Exit, Transfer)
    TRANSACTION_TYPES = [
        ('entry', 'Entry'),
        ('exit', 'Exit'),
        ('transfer', 'Transfer'),
    ]
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)

    # Transaction quantity (can be positive or negative)
    quantity = models.IntegerField()

    # Transaction date
    transaction_date = models.DateTimeField()

    # Transaction description (details such as why it was made, by whom)
    description = models.TextField(blank=True, null=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='warehouse_transaction_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='warehouse_transaction_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id}: {self.transaction_type} - {self.quantity}"
