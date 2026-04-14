# MIT License
#
# Copyright (c) 2025-2026 Ferhat Mousavi

from __future__ import annotations

import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from .company_permissions import (
    active_deletion_request,
    is_admin,
    is_owner,
    is_privileged,
    membership_for,
    owner_count,
    owner_user_ids,
    record_deletion_approval,
    try_complete_company_deletion,
)
from .forms import CompanyCreateForm, CompanyJoinForm, GrantOwnerForm
from .models import (
    Company,
    CompanyDeletionRequest,
    CompanyJoinRequest,
    CompanyMembership,
)

User = get_user_model()


def _make_unique_slug(name: str) -> str:
    base = (slugify(name) or "company")[:80]
    candidate = base
    while Company.objects.filter(slug=candidate).exists():
        candidate = f"{base}-{secrets.token_hex(3)}"[:96]
    return candidate


@login_required
def company_list(request: HttpRequest) -> HttpResponse:
    memberships = (
        CompanyMembership.objects.filter(user=request.user)
        .select_related("company")
        .order_by("company__name")
    )
    return render(
        request,
        "web_ui_app/company_list.html",
        {"memberships": memberships},
    )


@login_required
def company_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            slug = _make_unique_slug(name)
            with transaction.atomic():
                company = Company.objects.create(name=name, slug=slug)
                CompanyMembership.objects.create(
                    company=company,
                    user=request.user,
                    is_owner=True,
                    is_admin=True,
                )
            messages.success(request, f"Company “{company.name}” was created. Share slug: {company.slug}")
            return redirect("company_detail", slug=company.slug)
    else:
        form = CompanyCreateForm()
    return render(request, "web_ui_app/company_create.html", {"form": form})


@login_required
def company_join(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CompanyJoinForm(request.POST)
        if form.is_valid():
            slug = form.cleaned_data["slug"].strip()
            company = Company.objects.filter(slug__iexact=slug).first()
            if not company:
                messages.error(request, "No company matches that slug.")
            elif CompanyMembership.objects.filter(company=company, user=request.user).exists():
                messages.info(request, "You are already a member of this company.")
                return redirect("company_detail", slug=company.slug)
            elif CompanyJoinRequest.objects.filter(
                company=company,
                user=request.user,
                status=CompanyJoinRequest.Status.PENDING,
            ).exists():
                messages.info(request, "You already have a pending request for this company.")
            else:
                CompanyJoinRequest.objects.create(
                    company=company,
                    user=request.user,
                    message=form.cleaned_data.get("message", "").strip(),
                )
                messages.success(
                    request,
                    "Your request was submitted. An owner or administrator can approve it.",
                )
                return redirect("company_list")
    else:
        form = CompanyJoinForm()
    return render(request, "web_ui_app/company_join.html", {"form": form})


@login_required
def company_detail(request: HttpRequest, slug: str) -> HttpResponse:
    company = get_object_or_404(Company, slug=slug)
    m_self = membership_for(request.user, company)
    if not m_self:
        raise Http404()
    members = (
        CompanyMembership.objects.filter(company=company)
        .select_related("user")
        .order_by("user__username")
    )
    pending_joins = []
    if is_privileged(m_self):
        pending_joins = list(
            CompanyJoinRequest.objects.filter(
                company=company,
                status=CompanyJoinRequest.Status.PENDING,
            ).select_related("user")
        )
    del_req = active_deletion_request(company)
    owners = owner_user_ids(company)
    approved_ids: set[int] = set()
    if del_req:
        approved_ids = set(del_req.approvals.values_list("owner_user_id", flat=True))
    grant_owner_form = GrantOwnerForm() if is_owner(m_self) else None
    return render(
        request,
        "web_ui_app/company_detail.html",
        {
            "company": company,
            "m_self": m_self,
            "members": members,
            "pending_joins": pending_joins,
            "deletion_request": del_req,
            "owner_ids": owners,
            "deletion_approved_ids": approved_ids,
            "deletion_approved_count": len(approved_ids),
            "owner_total": len(owners),
            "grant_owner_form": grant_owner_form,
        },
    )


def _company_and_membership(request: HttpRequest, slug: str) -> tuple[Company, CompanyMembership]:
    company = get_object_or_404(Company, slug=slug)
    m = membership_for(request.user, company)
    if not m:
        raise Http404()
    return company, m


@login_required
@require_POST
def company_join_approve(request: HttpRequest, slug: str, pk: int) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    if not is_privileged(m):
        messages.error(request, "You cannot approve join requests for this company.")
        return redirect("company_detail", slug=slug)
    jr = get_object_or_404(
        CompanyJoinRequest,
        pk=pk,
        company=company,
        status=CompanyJoinRequest.Status.PENDING,
    )
    with transaction.atomic():
        jr.status = CompanyJoinRequest.Status.APPROVED
        jr.resolved_by = request.user
        from django.utils import timezone

        jr.resolved_at = timezone.now()
        jr.save(
            update_fields=("status", "resolved_by", "resolved_at"),
        )
        CompanyMembership.objects.get_or_create(
            company=company,
            user=jr.user,
            defaults={"is_owner": False, "is_admin": False},
        )
    messages.success(request, f"Approved {jr.user.username} as a member.")
    return redirect("company_detail", slug=slug)


@login_required
@require_POST
def company_join_reject(request: HttpRequest, slug: str, pk: int) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    if not is_privileged(m):
        messages.error(request, "You cannot reject join requests for this company.")
        return redirect("company_detail", slug=slug)
    jr = get_object_or_404(
        CompanyJoinRequest,
        pk=pk,
        company=company,
        status=CompanyJoinRequest.Status.PENDING,
    )
    from django.utils import timezone

    jr.status = CompanyJoinRequest.Status.REJECTED
    jr.resolved_by = request.user
    jr.resolved_at = timezone.now()
    jr.save(update_fields=("status", "resolved_by", "resolved_at"))
    messages.info(request, "Join request was rejected.")
    return redirect("company_detail", slug=slug)


@login_required
@require_POST
def company_grant_admin(request: HttpRequest, slug: str, user_id: int) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    if not is_privileged(m):
        messages.error(request, "Only owners or administrators can grant administrator.")
        return redirect("company_detail", slug=slug)
    target = get_object_or_404(CompanyMembership, company=company, user_id=user_id)
    if target.is_admin:
        messages.info(request, "That member is already an administrator.")
    else:
        target.is_admin = True
        target.save(update_fields=("is_admin",))
        messages.success(request, "Administrator access granted.")
    return redirect("company_detail", slug=slug)


@login_required
@require_POST
def company_revoke_admin(request: HttpRequest, slug: str, user_id: int) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    target = get_object_or_404(CompanyMembership, company=company, user_id=user_id)
    if target.is_owner:
        messages.error(request, "Cannot change administrator flag on an owner from here.")
        return redirect("company_detail", slug=slug)
    if not target.is_admin:
        messages.info(request, "That user is not an administrator.")
        return redirect("company_detail", slug=slug)
    if is_owner(m):
        pass
    elif is_admin(m) and m.user_id != target.user_id and is_admin(target):
        pass
    else:
        messages.error(
            request,
            "Only another administrator can revoke administrator from a peer, or an owner may revoke it.",
        )
        return redirect("company_detail", slug=slug)
    if is_admin(m) and not is_owner(m) and m.user_id == target.user_id:
        messages.error(request, "Use another administrator or an owner to revoke your own administrator access.")
        return redirect("company_detail", slug=slug)
    target.is_admin = False
    target.save(update_fields=("is_admin",))
    messages.success(request, "Administrator access removed.")
    return redirect("company_detail", slug=slug)


@login_required
@require_POST
def company_grant_owner(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    if not is_owner(m):
        messages.error(request, "Only an owner can assign the ownership tag.")
        return redirect("company_detail", slug=slug)
    form = GrantOwnerForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Enter a valid username.")
        return redirect("company_detail", slug=slug)
    username = form.cleaned_data["username"].strip()
    user = User.objects.filter(username__iexact=username).first()
    if not user:
        messages.error(request, "No user with that username.")
        return redirect("company_detail", slug=slug)
    target, _created = CompanyMembership.objects.get_or_create(
        company=company,
        user=user,
        defaults={"is_owner": False, "is_admin": False},
    )
    if target.is_owner:
        messages.info(request, "That member already has the ownership tag.")
    else:
        target.is_owner = True
        target.is_admin = True
        target.save(update_fields=("is_owner", "is_admin"))
        messages.success(request, f"Ownership tag assigned to {user.username}.")
    return redirect("company_detail", slug=slug)


@login_required
@require_POST
def company_self_remove_owner(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    if not m.is_owner:
        messages.error(request, "You are not an owner of this company.")
        return redirect("company_detail", slug=slug)
    if owner_count(company) < 2:
        messages.error(
            request,
            "This company must keep at least one owner. Add another owner or delete the company instead.",
        )
        return redirect("company_detail", slug=slug)
    m.is_owner = False
    m.save(update_fields=("is_owner",))
    messages.success(request, "You removed your ownership tag. Your other roles are unchanged.")
    return redirect("company_detail", slug=slug)


@login_required
@require_POST
def company_delete_initiate(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    if not is_owner(m):
        messages.error(request, "Only owners can start company deletion.")
        return redirect("company_detail", slug=slug)
    if active_deletion_request(company):
        messages.info(request, "A deletion approval is already in progress.")
        return redirect("company_detail", slug=slug)
    with transaction.atomic():
        req = CompanyDeletionRequest.objects.create(
            company=company,
            requested_by=request.user,
        )
        record_deletion_approval(req, request.user)
    if try_complete_company_deletion(company):
        messages.success(request, "The company was deleted.")
        return redirect("company_list")
    messages.warning(
        request,
        "Deletion started. Every owner must approve before the company is removed.",
    )
    return redirect("company_detail", slug=slug)


@login_required
@require_POST
def company_delete_approve(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = _company_and_membership(request, slug)
    if not is_owner(m):
        messages.error(request, "Only owners can approve deletion.")
        return redirect("company_detail", slug=slug)
    req = active_deletion_request(company)
    if not req:
        messages.info(request, "There is no pending deletion to approve.")
        return redirect("company_detail", slug=slug)
    record_deletion_approval(req, request.user)
    if try_complete_company_deletion(company):
        messages.success(request, "All owners approved. The company was deleted.")
        return redirect("company_list")
    messages.success(request, "Your approval was recorded.")
    return redirect("company_detail", slug=slug)
