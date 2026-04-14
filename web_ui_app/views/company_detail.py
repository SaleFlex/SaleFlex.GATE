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
