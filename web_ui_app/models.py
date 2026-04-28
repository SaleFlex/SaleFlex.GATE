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


class UserProfile(models.Model):
    """Optional web UI data for Django auth users (avatar, future fields)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="web_profile",
    )
    avatar = models.FileField(
        upload_to="web_ui_app/avatars/%Y/%m/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=("jpg", "jpeg", "png", "gif", "webp"),
            )
        ],
        help_text="Optional profile picture for the portal header (JPG, PNG, GIF, or WebP).",
    )

    def __str__(self) -> str:
        return f"Profile for {self.user_id}"


class Company(models.Model):
    """Portal tenant (hub company). Distinct from pos_api_app.Merchant until linked."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=96, unique=True, db_index=True)
    # Optional registration details (aligned with typical UK limited-company data; only name is required)
    companies_house_number = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="Companies House number",
        help_text="Company registration number (CRN) from Companies House, if applicable.",
    )
    vat_number = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="VAT number",
        help_text="VAT registration number, if applicable.",
    )
    registered_office = models.TextField(
        blank=True,
        verbose_name="Registered office address",
        help_text="Registered office or principal trading address, if recorded.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def has_registration_details(self) -> bool:
        return bool(
            self.companies_house_number
            or self.vat_number
            or self.registered_office
        )


class CompanyMembership(models.Model):
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


class CompanyJoinRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="join_requests",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_join_requests",
    )
    message = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_company_join_requests",
    )

    class Meta:
        ordering = ("-created_at",)


class CompanyDeletionRequest(models.Model):
    """When all current owners have approved, the company is deleted."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="deletion_requests",
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="initiated_company_deletions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)


class CompanyDeletionApproval(models.Model):
    deletion_request = models.ForeignKey(
        CompanyDeletionRequest,
        on_delete=models.CASCADE,
        related_name="approvals",
    )
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_deletion_approvals",
    )
    approved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("deletion_request", "owner_user"),
                name="uniq_deletion_approval_owner",
            ),
        ]
