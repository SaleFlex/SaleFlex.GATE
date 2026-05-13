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

"""
Load idempotent reference data after migrations (App Engine / Cloud Build friendly).

Usage::

    python manage.py seed_reference_data
    python manage.py seed_reference_data --only countries
    python manage.py seed_reference_data --dry-run

Add new datasets by implementing a function in ``core/seeders/`` and registering it in ``SEEDERS`` below.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from django.core.management.base import BaseCommand

from core.seeders import seed_countries

SeedFn = Callable[..., tuple[int, int]]

# Order matters: run cheap / foundational rows first.
SEEDERS: dict[str, SeedFn] = {
    "countries": seed_countries,
}


class Command(BaseCommand):
    help = "Insert or update reference rows (countries, …) for an empty or existing database."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--only",
            default="all",
            choices=["all", *sorted(SEEDERS)],
            help="Limit to one dataset (more values will appear as new seeders are added).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would run without writing to the database.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        only: str = options["only"]
        dry_run: bool = options["dry_run"]

        names = list(SEEDERS) if only == "all" else [only]

        for name in names:
            fn = SEEDERS[name]
            self.stdout.write(f"Seeding: {name} …")
            fn(dry_run=dry_run, stdout=self.stdout)

        if not dry_run:
            self.stdout.write(self.style.SUCCESS("Reference data seed finished."))
        else:
            self.stdout.write(self.style.WARNING("Dry run complete; no changes saved."))
