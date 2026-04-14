# MIT License
#
# Copyright (c) 2025-2026 Ferhat Mousavi

from __future__ import annotations

from django.contrib.auth.models import User

from .models import (
    Company,
    CompanyDeletionApproval,
    CompanyDeletionRequest,
    CompanyMembership,
)


def membership_for(user: User, company: Company) -> CompanyMembership | None:
    if not user.is_authenticated:
        return None
    return (
        CompanyMembership.objects.filter(company=company, user=user).select_related("user").first()
    )


def is_owner(m: CompanyMembership | None) -> bool:
    return bool(m and m.is_owner)


def is_admin(m: CompanyMembership | None) -> bool:
    return bool(m and m.is_admin)


def is_privileged(m: CompanyMembership | None) -> bool:
    """Owner or company admin: full portal operations except owner-only rules."""
    return is_owner(m) or is_admin(m)


def owner_user_ids(company: Company) -> set[int]:
    return set(
        CompanyMembership.objects.filter(company=company, is_owner=True).values_list(
            "user_id", flat=True
        )
    )


def owner_count(company: Company) -> int:
    return len(owner_user_ids(company))


def active_deletion_request(company: Company) -> CompanyDeletionRequest | None:
    return (
        CompanyDeletionRequest.objects.filter(company=company, completed_at__isnull=True)
        .order_by("-created_at")
        .first()
    )


def try_complete_company_deletion(company: Company) -> bool:
    """
    If every current owner has recorded approval on the active deletion request,
    delete the company. Returns True if deletion ran.
    """
    req = active_deletion_request(company)
    if not req:
        return False
    owners = owner_user_ids(company)
    if not owners:
        return False
    approved = set(
        CompanyDeletionApproval.objects.filter(deletion_request=req).values_list(
            "owner_user_id", flat=True
        )
    )
    if owners <= approved:
        company.delete()
        return True
    return False


def record_deletion_approval(req: CompanyDeletionRequest, user: User) -> None:
    CompanyDeletionApproval.objects.get_or_create(
        deletion_request=req,
        owner_user=user,
    )
