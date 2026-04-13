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

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from pos_api_app.models.merchant_api_token import MerchantAPIToken


class MerchantTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Expect the token in the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Split the token from the 'Bearer' scheme
        try:
            token_key = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Invalid token header. No token provided.')

        # Try to find the token in the database
        try:
            token = MerchantAPIToken.objects.get(token=token_key, is_active=True)
        except MerchantAPIToken.DoesNotExist:
            raise AuthenticationFailed('Invalid or expired token.')

        # Optionally, check if the token has expired
        if token.has_expired():
            raise AuthenticationFailed('Token has expired.')

        # Return the merchant and token for DRF's request.user and request.auth
        return token.merchant, token

    def authenticate_header(self, request):
        return 'Bearer'
