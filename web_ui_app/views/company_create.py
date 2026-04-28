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
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..forms import CompanyCreateForm, registration_kwargs_from_cleaned
from ..models import Company, CompanyMembership
from .company_helpers import make_unique_slug


@login_required
def company_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CompanyCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"].strip()
            slug = make_unique_slug(name)
            with transaction.atomic():
                company = Company.objects.create(
                    name=name,
                    slug=slug,
                    **registration_kwargs_from_cleaned(form.cleaned_data),
                )
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
