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

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from .base import BaseModel


class AbstractCashier(AbstractUser, BaseModel):
    """
    Django auth user and universal SaleFlex identity for GATE, OFFICE, PyPOS, and mPOS.

    Company-scoped roles (owner, admin, store manager, POS cashier, OFFICE access)
    are stored on ``CompanyMembership`` so the same person can differ by company.
    Per-store POS device authorisation is on ``CashierStoreAssignment``.
    """

    avatar = models.FileField(
        upload_to="gate/avatars/%Y/%m/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=("jpg", "jpeg", "png", "gif", "webp"),
            )
        ],
        help_text="Optional profile picture shown in the portal header and synced to client apps.",
    )
    cashier_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Numeric cashier ID used by PyPOS and OFFICE for transaction attribution.",
    )
    pin_code = models.CharField(
        max_length=8,
        blank=True,
        help_text="Short numeric PIN used for quick login on POS / kitchen / mPOS screens.",
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft-delete flag; records are retained for audit purposes.",
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.username

    @property
    def display_name(self) -> str:
        full = self.get_full_name()
        return full if full else self.username

    def get_store_assignments(self):
        """Return all active CashierStoreAssignment records for this cashier."""
        return self.store_assignments.filter(is_active=True)

    def get_accessible_pos_devices(self, store):
        """
        Return the POS devices this cashier can access in a specific store.
        Delegates to the matching CashierStoreAssignment, if any.
        """
        assignment = self.store_assignments.filter(store=store, is_active=True).first()
        if assignment is None:
            return type(store).pos_devices.rel.related_model.objects.none()
        return assignment.get_accessible_pos_devices()
