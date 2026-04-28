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


class Cashier(models.Model):
    """
    Represents a cashier who can operate POS devices in a store.
    Cashiers can either operate on all POS devices within a store, or be restricted
    to specific POS devices.
    """

    # Foreign key to the User model (represents the user associated with this cashier)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cashier_profile')

    # The store where the cashier works (a cashier can work in one store)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='cashiers')

    # Optional: Specific POS devices that the cashier is allowed to use (can be empty if cashier can use all POS devices)
    pos_devices = models.ManyToManyField('PointOfSale', related_name='authorized_cashiers', blank=True)

    # Indicates if the cashier can use all POS devices in the store
    can_access_all_pos = models.BooleanField(default=False)

    # Indicates if the cashier is active or inactive
    is_active = models.BooleanField(default=True)

    # Indicates if the cashier has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='cashier_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='cashier_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Cashier'
        unique_together = ('user', 'store')  # Ensures a cashier works in one store at a time

    def __str__(self):
        return f"{self.user.username} - {self.store.name}"

    def get_accessible_pos_devices(self):
        """
        Returns the POS devices the cashier can access.
        If `can_access_all_pos` is True, returns all POS devices in the store.
        Otherwise, returns the specific POS devices assigned to the cashier.
        """
        if self.can_access_all_pos:
            return self.store.pos_devices.all()
        return self.pos_devices.all()
