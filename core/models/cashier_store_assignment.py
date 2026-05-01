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

from django.conf import settings
from django.db import models


class CashierStoreAssignment(models.Model):
    """
    Grants a GateUser access to a specific store and optionally to a subset
    of its POS devices.

    A single GateUser may have assignments in multiple stores (multi-store
    support). The GateUser.is_cashier flag indicates the role at the ecosystem
    level; this model records which store(s) and device(s) they can actually
    operate.

    When can_access_all_pos is True the pos_devices M2M is ignored and the
    user may open any active POS terminal in that store.
    """

    gate_user = models.ForeignKey(
        "GateUser",
        on_delete=models.CASCADE,
        related_name="store_assignments",
        help_text="The GateUser being assigned to this store.",
    )
    store = models.ForeignKey(
        "Store",
        on_delete=models.CASCADE,
        related_name="cashier_assignments",
        help_text="Store where the user is authorised to operate.",
    )
    pos_devices = models.ManyToManyField(
        "PointOfSale",
        related_name="cashier_assignments",
        blank=True,
        help_text="Specific POS devices the user may use. Ignored when can_access_all_pos is True.",
    )
    can_access_all_pos = models.BooleanField(
        default=False,
        help_text="When True the user may operate every active POS in the store.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive assignments are ignored by all applications.",
    )

    # Audit trail
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="cashier_assignment_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="cashier_assignment_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "CashierStoreAssignment"
        verbose_name = "Cashier store assignment"
        verbose_name_plural = "Cashier store assignments"
        constraints = [
            models.UniqueConstraint(
                fields=("gate_user", "store"),
                name="uniq_gate_user_store_assignment",
            )
        ]

    def __str__(self) -> str:
        return f"{self.gate_user} @ {self.store}"

    def get_accessible_pos_devices(self):
        """
        Return the POS devices this assignment authorises.
        If can_access_all_pos is True, returns all active POS devices in the store.
        Otherwise returns the explicitly assigned subset.
        """
        if self.can_access_all_pos:
            return self.store.pos_devices.filter(is_active=True)
        return self.pos_devices.all()
