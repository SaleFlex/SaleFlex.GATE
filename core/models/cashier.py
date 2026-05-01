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
from django.core.validators import FileExtensionValidator
from django.db import models


class GateUser(models.Model):
    """
    Universal profile for every person in the SaleFlex ecosystem.

    One GateUser record exists per Django auth User. It is the single source of
    truth for identity fields that are shared across GATE (web portal),
    SaleFlex.OFFICE, SaleFlex.PyPOS, and SaleFlex.mPOS. When those applications
    authenticate against GATE they receive a subset of these fields as their
    user/cashier payload.

    Role flags are not mutually exclusive: a company owner is also typically an
    admin; a store manager may also act as a cashier on the floor.
    Store-level POS device authorisation is held separately in
    CashierStoreAssignment so that one user can work across multiple stores.
    """

    # --- Identity anchor ---
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gate_user",
        help_text="Django auth user this profile belongs to.",
    )

    # --- Portal / web UI fields ---
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

    # --- POS / operations fields (synced to PyPOS, OFFICE, mPOS) ---
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

    # --- System-wide role flags ---
    # These are ecosystem-level roles. Store-level authorisation is in CashierStoreAssignment.
    is_cashier = models.BooleanField(
        default=False,
        help_text="Can operate POS terminals. Authorised stores/devices are in CashierStoreAssignment.",
    )
    is_store_manager = models.BooleanField(
        default=False,
        help_text="Can manage store configuration, staff, and reports for assigned stores.",
    )
    is_office_user = models.BooleanField(
        default=False,
        help_text="Can log in to SaleFlex.OFFICE (back-office / ERP screens).",
    )
    is_company_admin = models.BooleanField(
        default=False,
        help_text="Company-level administrator: full portal operations for their company.",
    )
    is_company_owner = models.BooleanField(
        default=False,
        help_text="Company owner tag: required to start/approve company deletion; assignable only by another owner.",
    )

    # --- Status ---
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive users cannot log in to any SaleFlex application.",
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft-delete flag; records are retained for audit purposes.",
    )

    # --- Audit trail ---
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="gate_user_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="gate_user_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "GateUser"
        verbose_name = "Gate user"
        verbose_name_plural = "Gate users"

    def __str__(self) -> str:
        return self.user.username

    @property
    def display_name(self) -> str:
        """Full name when available, username otherwise."""
        full = self.user.get_full_name()
        return full if full else self.user.username

    def get_store_assignments(self):
        """Return all active CashierStoreAssignment records for this user."""
        return self.store_assignments.filter(is_active=True)

    def get_accessible_pos_devices(self, store):
        """
        Return the POS devices this user can access in a specific store.
        Delegates to the matching CashierStoreAssignment, if any.
        """
        assignment = self.store_assignments.filter(store=store, is_active=True).first()
        if assignment is None:
            return type(store).pos_devices.rel.related_model.objects.none()
        return assignment.get_accessible_pos_devices()
