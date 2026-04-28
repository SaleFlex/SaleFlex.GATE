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

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from ..company_permissions import (
    active_deletion_request,
    is_owner,
    is_privileged,
    membership_for,
    owner_user_ids,
)
from ..forms import CompanyRegistrationForm, GrantOwnerForm
from ..models import Company, CompanyJoinRequest, CompanyMembership


@login_required
def company_detail(request: HttpRequest, slug: str) -> HttpResponse:
    company = get_object_or_404(Company, slug=slug)
    m_self = membership_for(request.user, company)
    if not m_self:
        raise Http404()
    if request.method == "POST" and request.POST.get("form_id") == "company_registration":
        if not is_privileged(m_self):
            messages.error(request, "You cannot edit company details.")
            return redirect("company_detail", slug=company.slug)
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
    registration_form = None
    if is_privileged(m_self):
        if request.method == "POST" and request.POST.get("form_id") == "company_registration":
            registration_form = CompanyRegistrationForm(request.POST, instance=company)
            if registration_form.is_valid():
                registration_form.save()
                messages.success(request, "Company details were updated.")
                return redirect("company_detail", slug=company.slug)
        if registration_form is None:
            registration_form = CompanyRegistrationForm(instance=company)
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
            "registration_form": registration_form,
        },
    )
