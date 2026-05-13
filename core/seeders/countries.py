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

"""Load ``Country`` rows from ISO 3166-1 via pycountry."""

from __future__ import annotations

from typing import TextIO

import pycountry
from babel.numbers import get_territory_currencies
from django.db import transaction

from core.models import Country


def _primary_currency_code(iso_alpha2: str) -> str:
    """
    Territory (ISO alpha-2) → single ISO 4217 code using Babel CLDR data.

    If multiple currencies are tied to a territory (e.g. CH), returns one deterministic pick.
    Empty string means no CLDR assignment (often overseas / special territories).
    """
    a2 = (iso_alpha2 or "").strip().upper()
    if len(a2) != 2:
        return ""
    try:
        codes = get_territory_currencies(a2)
    except (LookupError, KeyError):
        return ""
    if not codes:
        return ""
    return sorted(str(c) for c in codes)[0][:3]


def seed_countries(
    *,
    dry_run: bool = False,
    stdout: TextIO | None = None,
) -> tuple[int, int]:
    """
    Upsert ISO 3166-1 countries into ``Country`` using ``iso_alpha2`` as the natural key.

    Fills ``name``, ``code`` (alpha-2), ``short_name`` (alpha-3), ``iso_*``, and ``currency_code``
    from Babel territory→currency mappings (Unicode CLDR) where available.

    Re-running replaces those fields via ``defaults`` when using ``seed_reference_data``.

    Returns ``(created_count, updated_count)``. For ``dry_run``, returns ``(0, 0)`` after printing the row count.
    """
    max_name = Country._meta.get_field("name").max_length

    rows: list[tuple[str, dict]] = []
    for c in sorted(pycountry.countries, key=lambda x: (x.alpha_2 or "").lower()):
        a2 = c.alpha_2
        if not a2:
            continue
        name = (c.name or "").strip()
        if not name:
            continue
        raw_num = getattr(c, "numeric", None) or ""
        numeric_s = raw_num.zfill(3)[:3] if raw_num else ""
        cc = _primary_currency_code(a2)
        defaults: dict = {
            "name": name[:max_name],
            "code": a2,
            "short_name": (c.alpha_3 or "")[:50],
            "iso_alpha2": a2,
            "iso_alpha3": ((c.alpha_3 or "")[:3]),
            "iso_numeric": numeric_s,
            "currency_code": cc,
            "is_deleted": False,
        }
        rows.append((a2, defaults))

    if dry_run:
        if stdout:
            stdout.write(f"[dry-run] Would upsert {len(rows)} countries (key=iso_alpha2).\n")
        return 0, 0

    created = 0
    updated = 0
    with transaction.atomic():
        for a2, defaults in rows:
            _obj, did_create = Country.objects.update_or_create(
                iso_alpha2=a2,
                defaults=defaults,
            )
            if did_create:
                created += 1
            else:
                updated += 1

    if stdout:
        stdout.write(
            f"Countries: created={created}, updated={updated} (unique ISO alpha-2 rows={len(rows)}).\n"
        )

    return created, updated
