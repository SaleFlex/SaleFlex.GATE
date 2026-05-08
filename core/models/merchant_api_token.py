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

import uuid

from django.db import models
from django.utils import timezone

from .base import BaseModel


class MerchantAPIToken(BaseModel):
    # Token value (using UUID for uniqueness)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Link the token to a specific merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name='api_tokens')

    # Expiration date of the token (optional, you can use this to set token lifetimes)
    expires_at = models.DateTimeField(null=True, blank=True)

    # Indicates if the token is active or revoked
    is_active = models.BooleanField(default=True)

    # Indicates if the token has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    def has_expired(self):
        """Checks if the token has expired based on the current time and expiration date."""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def __str__(self):
        return f"Token for {self.merchant.name} - {self.token}"

    class Meta:
        db_table = 'MerchantAPIToken'
        verbose_name = 'Merchant API Token'
        verbose_name_plural = 'Merchant API Tokens'
