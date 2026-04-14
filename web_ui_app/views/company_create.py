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
