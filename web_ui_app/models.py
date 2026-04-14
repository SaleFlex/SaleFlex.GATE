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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


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
