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

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Company, CompanyJoinRequest, CompanyMembership


class PortalPasswordChangeTests(TestCase):
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


class PortalCompanyTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner1", password="pass-owner-1")
        self.other = User.objects.create_user("member1", password="pass-member-1")

    def test_create_company_makes_owner_and_admin(self):
        self.client.login(username="owner1", password="pass-owner-1")
        r = self.client.post(
            reverse("company_create"),
            {"name": "Acme Retail"},
            follow=False,
        )
        self.assertEqual(r.status_code, 302)
        c = Company.objects.get(name="Acme Retail")
        m = CompanyMembership.objects.get(company=c, user=self.owner)
        self.assertTrue(m.is_owner)
        self.assertTrue(m.is_admin)

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
