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

from django.forms.utils import flatatt
from django.forms.widgets import EmailInput, PasswordInput, TextInput
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


class AtomicPasswordInput(_AtomicInputMixin, PasswordInput):
    pass


class AtomicEmailInput(_AtomicInputMixin, EmailInput):
    pass
