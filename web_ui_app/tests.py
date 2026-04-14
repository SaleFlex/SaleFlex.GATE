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
