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
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..company_permissions import (
    active_deletion_request,
    is_owner,
    record_deletion_approval,
    try_complete_company_deletion,
)
from ..models import CompanyDeletionRequest
from .company_helpers import company_and_membership


@login_required
@require_POST
def company_delete_initiate(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = company_and_membership(request, slug)
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
