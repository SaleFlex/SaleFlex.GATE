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
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..forms import CompanyJoinForm
from ..models import Company, CompanyJoinRequest, CompanyMembership


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
