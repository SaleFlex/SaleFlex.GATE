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

import secrets

from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from ..company_permissions import membership_for
from ..models import Company, CompanyMembership


def make_unique_slug(name: str) -> str:
    base = (slugify(name) or "company")[:80]
    candidate = base
    while Company.objects.filter(slug=candidate).exists():
        candidate = f"{base}-{secrets.token_hex(3)}"[:96]
    return candidate


def company_and_membership(request: HttpRequest, slug: str) -> tuple[Company, CompanyMembership]:
    company = get_object_or_404(Company, slug=slug)
    m = membership_for(request.user, company)
    if not m:
        raise Http404()
    return company, m
