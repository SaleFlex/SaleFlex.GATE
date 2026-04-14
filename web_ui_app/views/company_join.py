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
