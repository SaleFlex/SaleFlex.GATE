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
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..company_permissions import (
    active_deletion_request,
    is_owner,
    record_deletion_approval,
    try_complete_company_deletion,
)
from .company_helpers import company_and_membership


@login_required
@require_POST
def company_delete_approve(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = company_and_membership(request, slug)
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
