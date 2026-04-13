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

import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class MerchantAPIToken(models.Model):
    # Token value (using UUID for uniqueness)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Link the token to a specific merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name='api_tokens')

    # Date and time when the token was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Expiration date of the token (optional, you can use this to set token lifetimes)
    expires_at = models.DateTimeField(null=True, blank=True)

    # Indicates if the token is active or revoked
    is_active = models.BooleanField(default=True)

    # Indicates if the token has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Foreign key to the User model, to track who created the token (optional)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='token_created')

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
