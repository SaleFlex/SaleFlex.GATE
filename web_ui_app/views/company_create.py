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

from ..forms import (
    PORTAL_SESSION_COUNTRY_PK,
    WIZARD_STEP_COUNTRY,
    WIZARD_STEP_DETAILS,
    CompanyCreateForm,
    CompanyWizardCountryStepForm,
    active_template_for_country,
    merged_registration_defs,
    portal_active_countries,
    registration_kwargs_from_cleaned,
)
from core.models import Country

from ..models import Company, CompanyMembership
from .company_helpers import make_unique_slug


def _hints_for_country_and_template(selected_country: Country | None, template):  # CountryTemplate | None
    hints: dict = {"currency_code": "", "languages": [], "vat_rates_display": [], "measurement_unit_system": ""}
    if not selected_country:
        return hints
    if template and template.default_currency_code:
        hints["currency_code"] = template.default_currency_code.strip().upper()
    elif selected_country.currency_code:
        hints["currency_code"] = (selected_country.currency_code or "").strip().upper()
    langs = []
    if template and template.language_tags and isinstance(template.language_tags, list):
        langs.extend(str(x).strip() for x in template.language_tags if x)
    if not langs:
        iso = getattr(selected_country, "iso_culture_code", None)
        if iso:
            langs.append(iso.strip())
    if (
        not langs
        and selected_country.languages
        and isinstance(selected_country.languages, list)
    ):
        langs.extend(str(x).strip() for x in selected_country.languages if x)
    hints["languages"] = langs
    hints["measurement_unit_system"] = getattr(template, "measurement_unit_system", "") if template else ""
    if template and template.vat_rates and isinstance(template.vat_rates, list):
        rows = []
        for item in template.vat_rates:
            if not isinstance(item, dict):
                continue
            lbl = item.get("label") or item.get("code") or ""
            pct = item.get("rate_percent")
            rate_display = None
            if pct is not None and str(pct).strip() != "":
                raw = str(pct).strip()
                rate_display = raw if raw.endswith("%") else f"{raw}%"
            if lbl or rate_display:
                rows.append({"label": str(lbl).strip(), "rate_display": rate_display})
        hints["vat_rates_display"] = rows
    return hints


def _intro_for_wizard(selected_country: Country | None, template) -> str:
    if template and (template.wizard_intro or "").strip():
        return (template.wizard_intro or "").strip()
    generic = (
        "You become an owner and administrator automatically. You can invite others with "
        "the company slug after it is created. Only the company name is required; "
        "optional fields cover registration details commonly used where you operate."
    )
    if selected_country:
        return f"{generic}\n\nSelected country: {selected_country.name}"
    return generic


def _render_step_country(request: HttpRequest, countries_qs, form: CompanyWizardCountryStepForm | None):
    if form is None:
        form = CompanyWizardCountryStepForm(countries_queryset=countries_qs)
    ctx = {
        "wizard_phase": WIZARD_STEP_COUNTRY,
        "country_form": form,
        "countries_qs_empty": not countries_qs.exists(),
        "countries_count": countries_qs.count(),
    }
    return render(request, "web_ui_app/company_create.html", ctx)


def _render_step_details(
    request: HttpRequest,
    selected_country: Country,
    template,
    form: CompanyCreateForm | None,
    *,
    errors_on_form: CompanyCreateForm | None = None,
):
    tmpl_defs = merged_registration_defs(template)
    if form is None:
        form = CompanyCreateForm(is_wizard=True, registration_defs=tmpl_defs)

    merged_ctx = {}
    merged_ctx.update(
        {
            "wizard_phase": WIZARD_STEP_DETAILS,
            "selected_country": selected_country,
            "country_template": template,
            "intro_text": _intro_for_wizard(selected_country, template),
            "hints": _hints_for_country_and_template(selected_country, template),
            "wizard_form": errors_on_form or form,
            "countries_qs_empty": False,
            "countries_count": 0,
        }
    )
    return render(request, "web_ui_app/company_create.html", merged_ctx)


@login_required
def company_create(request: HttpRequest) -> HttpResponse:
    sess = request.session
    if request.GET.get("restart"):
        sess.pop(PORTAL_SESSION_COUNTRY_PK, None)
        messages.info(request, "Choose a country to start again.")

    countries_qs = portal_active_countries()
    sess_country_pk = sess.get(PORTAL_SESSION_COUNTRY_PK)
    selected_country = None
    if sess_country_pk:
        selected_country = countries_qs.filter(pk=sess_country_pk).first()
        if selected_country is None:
            sess.pop(PORTAL_SESSION_COUNTRY_PK, None)
            sess_country_pk = None
            sess.modified = True
            messages.warning(request, "The previously selected country is no longer available.")

    template = active_template_for_country(selected_country)

    if request.method == "POST":
        step = request.POST.get("wizard_step")

        if step == WIZARD_STEP_COUNTRY:
            c_form = CompanyWizardCountryStepForm(request.POST, countries_queryset=countries_qs)
            if c_form.is_valid():
                cid = c_form.cleaned_data["country"].pk
                sess[PORTAL_SESSION_COUNTRY_PK] = int(cid)
                sess.modified = True
                return redirect("company_create")
            return _render_step_country(request, countries_qs, c_form)

        if step == WIZARD_STEP_DETAILS:
            if not selected_country:
                messages.warning(request, "Choose a country first.")
                return redirect("company_create")
            tmpl = active_template_for_country(selected_country)
            tmpl_defs = merged_registration_defs(tmpl)
            wiz_form = CompanyCreateForm(request.POST, is_wizard=True, registration_defs=tmpl_defs)
            if wiz_form.is_valid():
                name = wiz_form.cleaned_data["name"].strip()
                slug = make_unique_slug(name)
                with transaction.atomic():
                    company = Company.objects.create(
                        name=name,
                        slug=slug,
                        country=selected_country,
                        **registration_kwargs_from_cleaned(wiz_form.cleaned_data),
                    )
                    CompanyMembership.objects.create(
                        company=company,
                        user=request.user,
                        is_owner=True,
                        is_admin=True,
                        is_office_user=True,
                    )
                sess.pop(PORTAL_SESSION_COUNTRY_PK, None)
                sess.modified = True
                messages.success(
                    request,
                    f"Company “{company.name}” was created. Share slug: {company.slug}",
                )
                return redirect("company_detail", slug=company.slug)

            messages.error(request, "Fix the errors below.")
            return _render_step_details(
                request,
                selected_country,
                tmpl,
                None,
                errors_on_form=wiz_form,
            )

        messages.warning(
            request,
            "Continue with the onboarding steps below (pick a country, then enter company details).",
        )
        return redirect("company_create")

    if not selected_country:
        return _render_step_country(request, countries_qs, None)

    return _render_step_details(request, selected_country, template, None)
