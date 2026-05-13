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

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import Country, CountryTemplate

from .models import Company, CompanyJoinRequest, CompanyMembership

User = get_user_model()

# Offline compressor manifest is optional during tests; avoids requiring `compress` after every template change.
@override_settings(COMPRESS_OFFLINE=False)
class WebUiAppTestCase(TestCase):
    """Base for tests that render templates using {% compress %}."""


class PortalPasswordChangeTests(WebUiAppTestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="oldpass12345")

    def test_anonymous_redirects_to_login(self):
        r = self.client.get(reverse("password_change"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r["Location"])

    def test_post_updates_password_and_preserves_session(self):
        self.client.login(username="alice", password="oldpass12345")
        new_pw = "new-uncommon-pass-xyz-99"
        r = self.client.post(
            reverse("password_change"),
            {
                "old_password": "oldpass12345",
                "new_password1": new_pw,
                "new_password2": new_pw,
            },
        )
        self.assertRedirects(r, reverse("password_change_done"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_pw))
        dash = self.client.get(reverse("dashboard"))
        self.assertEqual(dash.status_code, 200)


class PortalCompanyTests(WebUiAppTestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner1", password="pass-owner-1")
        self.other = User.objects.create_user("member1", password="pass-member-1")
        self.country = Country.objects.create(
            name="United Kingdom",
            iso_alpha2="GB",
            currency_code="GBP",
            is_deleted=False,
        )

    def _complete_company_create_wizard(self, name: str, **optional_fields):
        url = reverse("company_create")
        r_country = self.client.post(
            url,
            {"wizard_step": "country", "country": str(self.country.pk)},
        )
        self.assertRedirects(r_country, url, fetch_redirect_response=False)
        payload = {"wizard_step": "details", "name": name, **optional_fields}
        return self.client.post(url, payload)

    def test_create_company_makes_owner_and_admin(self):
        self.client.login(username="owner1", password="pass-owner-1")
        r = self._complete_company_create_wizard("Acme Retail")
        self.assertEqual(r.status_code, 302)
        c = Company.objects.get(name="Acme Retail")
        self.assertEqual(c.country_id, self.country.pk)
        m = CompanyMembership.objects.get(company=c, user=self.owner)
        self.assertTrue(m.is_owner)
        self.assertTrue(m.is_admin)

    def test_create_company_saves_optional_registration_fields(self):
        self.client.login(username="owner1", password="pass-owner-1")
        r = self._complete_company_create_wizard(
            "Euro UK Ltd",
            companies_house_number="",
            vat_number="GB123456789",
            registered_office="1 Test St, London",
        )
        self.assertEqual(r.status_code, 302)
        c = Company.objects.get(name="Euro UK Ltd")
        self.assertEqual(c.vat_number, "GB123456789")
        self.assertEqual(c.registered_office, "1 Test St, London")

    def test_wizard_requires_country_selection_first(self):
        self.client.login(username="owner1", password="pass-owner-1")
        url = reverse("company_create")
        r = self.client.post(url, {"wizard_step": "details", "name": "Nobody Co"})
        self.assertRedirects(r, url)
        self.assertFalse(Company.objects.filter(name="Nobody Co").exists())

    def test_country_template_surfaces_intro_and_tax_hints(self):
        CountryTemplate.objects.create(
            country=self.country,
            wizard_intro="__WIZ_TMPL_MARKER__",
            vat_rates=[{"label": "Demo tax", "rate_percent": "20"}],
        )
        self.client.login(username="owner1", password="pass-owner-1")
        url = reverse("company_create")
        self.client.post(url, {"wizard_step": "country", "country": str(self.country.pk)})
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "__WIZ_TMPL_MARKER__")
        self.assertContains(r, "Demo tax")
        self.assertContains(r, "20%")

    def test_inactive_country_template_is_ignored_for_ui(self):
        CountryTemplate.objects.create(
            country=self.country,
            is_active=False,
            wizard_intro="__WIZ_DISABLED__",
            vat_rates=[{"label": "Hidden", "rate_percent": "99"}],
        )
        self.client.login(username="owner1", password="pass-owner-1")
        url = reverse("company_create")
        self.client.post(url, {"wizard_step": "country", "country": str(self.country.pk)})
        r = self.client.get(url)
        self.assertNotContains(r, "__WIZ_DISABLED__")

    def test_owner_updates_registration_on_company_detail(self):
        company = Company.objects.create(name="Co", slug="co-reg-test", country=self.country)
        CompanyMembership.objects.create(
            company=company,
            user=self.owner,
            is_owner=True,
            is_admin=True,
        )
        payload = {
            "form_id": "company_registration",
            "name": "Co Legal Name",
            "companies_house_number": "06548712",
            "vat_number": "",
            "registered_office": "",
        }
        self.client.login(username="owner1", password="pass-owner-1")
        r = self.client.post(reverse("company_detail", args=[company.slug]), payload)
        self.assertRedirects(r, reverse("company_detail", args=[company.slug]))
        company.refresh_from_db()
        self.assertEqual(company.name, "Co Legal Name")
        self.assertEqual(company.companies_house_number, "06548712")

    def test_plain_member_cannot_post_registration_update(self):
        company = Company.objects.create(
            name="Sec",
            slug="sec-test",
            vat_number="GB111111111",
        )
        CompanyMembership.objects.create(
            company=company,
            user=self.owner,
            is_owner=True,
            is_admin=True,
        )
        CompanyMembership.objects.create(
            company=company,
            user=self.other,
            is_owner=False,
            is_admin=False,
        )
        payload = {
            "form_id": "company_registration",
            "name": "Hacked",
            "companies_house_number": "",
            "vat_number": "GB999999999",
            "registered_office": "",
        }
        self.client.login(username="member1", password="pass-member-1")
        r = self.client.post(reverse("company_detail", args=[company.slug]), payload)
        self.assertRedirects(r, reverse("company_detail", args=[company.slug]))
        company.refresh_from_db()
        self.assertEqual(company.name, "Sec")
        self.assertEqual(company.vat_number, "GB111111111")

    def test_join_request_approve_adds_member(self):
        company = Company.objects.create(name="Co", slug="co-test")
        CompanyMembership.objects.create(
            company=company,
            user=self.owner,
            is_owner=True,
            is_admin=True,
        )
        jr = CompanyJoinRequest.objects.create(company=company, user=self.other)
        self.client.login(username="owner1", password="pass-owner-1")
        r = self.client.post(reverse("company_join_approve", args=[company.slug, jr.pk]))
        self.assertEqual(r.status_code, 302)
        jr.refresh_from_db()
        self.assertEqual(jr.status, CompanyJoinRequest.Status.APPROVED)
        m = CompanyMembership.objects.get(company=company, user=self.other)
        self.assertFalse(m.is_owner)
        self.assertFalse(m.is_admin)

    def test_two_owner_deletion_requires_both_approvals(self):
        company = Company.objects.create(name="Dual", slug="dual-test")
        CompanyMembership.objects.create(
            company=company,
            user=self.owner,
            is_owner=True,
            is_admin=True,
        )
        CompanyMembership.objects.create(
            company=company,
            user=self.other,
            is_owner=True,
            is_admin=True,
        )
        self.client.login(username="owner1", password="pass-owner-1")
        self.client.post(reverse("company_delete_initiate", args=[company.slug]))
        self.assertTrue(Company.objects.filter(pk=company.pk).exists())
        self.client.logout()
        self.client.login(username="member1", password="pass-member-1")
        self.client.post(reverse("company_delete_approve", args=[company.slug]))
        self.assertFalse(Company.objects.filter(pk=company.pk).exists())

    def test_non_member_cannot_open_company_detail(self):
        company = Company.objects.create(name="X", slug="x-test")
        CompanyMembership.objects.create(
            company=company,
            user=self.owner,
            is_owner=True,
            is_admin=True,
        )
        self.client.login(username="member1", password="pass-member-1")
        r = self.client.get(reverse("company_detail", args=[company.slug]))
        self.assertEqual(r.status_code, 404)


class PortalThemePickerTests(WebUiAppTestCase):
    """Gate web UI exposes Light / Dark / System theme (client-side, localStorage)."""

    def test_landing_includes_theme_picker_and_scripts(self):
        r = self.client.get(reverse("landing"))
        self.assertEqual(r.status_code, 200)
        content = r.content.decode()
        self.assertIn("data-theme-picker", content)
        self.assertIn("saleflex-gate-theme", content)
        self.assertRegex(
            content,
            r"gate/js/theme\.js|/files/CACHE/js/[^\"']+\.js",
            msg="Expect theme script via static path or offline compress bundle",
        )

    def test_dashboard_includes_theme_picker(self):
        user = get_user_model().objects.create_user("themer", password="pass-theme-1")
        self.client.login(username="themer", password="pass-theme-1")
        r = self.client.get(reverse("dashboard"))
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"data-theme-picker", r.content)
