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
