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

from django.forms.utils import flatatt
from django.forms.widgets import EmailInput, FileInput, PasswordInput, Textarea, TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class _AtomicInputMixin:
    """
    Build the <input> element in Python via format_html/flatatt instead of the
    default widget templates. Some environments were showing attribute text below
    the control as if the tag had been split; a single SafeString avoids that.
    """

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        w = context["widget"]
        attrs_dict = {**w["attrs"], "type": w["type"], "name": w["name"]}
        if w["value"] is not None:
            attrs_dict["value"] = w["value"]
        return format_html("<input{}>", mark_safe(flatatt(attrs_dict)))


class AtomicTextInput(_AtomicInputMixin, TextInput):
    pass


class AtomicTextarea(Textarea):
    """Same rationale as _AtomicInputMixin: single format_html for <textarea>."""

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        w = context["widget"]
        attrs_dict = {**w["attrs"], "name": w["name"]}
        val = w["value"] if w["value"] is not None else ""
        return format_html("<textarea{}>{}</textarea>", mark_safe(flatatt(attrs_dict)), val)


class AtomicPasswordInput(_AtomicInputMixin, PasswordInput):
    pass


class AtomicEmailInput(_AtomicInputMixin, EmailInput):
    pass


class AtomicFileInput(FileInput):
    """
    Same idea as _AtomicInputMixin: one format_html call so file inputs do not
    split into visible attribute text in some browsers / Django template setups.
    Never emit a value= attribute on file inputs.
    """

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        w = context["widget"]
        attrs_dict = {**w["attrs"], "type": w["type"], "name": w["name"]}
        return format_html("<input{}>", mark_safe(flatatt(attrs_dict)))
