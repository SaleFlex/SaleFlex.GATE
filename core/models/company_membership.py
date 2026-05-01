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

from .company import Company


class CompanyMembership(models.Model):
    """Links a user to a company with optional owner and administrator flags."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_memberships",
    )
    is_owner = models.BooleanField(
        default=False,
        help_text="Ownership tag: not removable by others; assignable only by an owner.",
    )
    is_admin = models.BooleanField(
        default=False,
        help_text="Company administrator: full portal operations except company delete and owner-tag changes on others.",
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("company", "user"),
                name="uniq_web_ui_company_membership_user",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user_id} @ {self.company_id}"
