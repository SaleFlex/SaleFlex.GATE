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
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ..company_permissions import is_privileged
from ..models import CompanyMembership
from .company_helpers import company_and_membership


@login_required
@require_POST
def company_grant_admin(request: HttpRequest, slug: str, user_id: int) -> HttpResponse:
    company, m = company_and_membership(request, slug)
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
