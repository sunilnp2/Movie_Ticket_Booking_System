from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomBasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the user credentials from the request headers
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        auth_type, auth_string = auth_header.split(' ')
        if auth_type.lower() != 'basic':
            return None

        try:
            username, password = auth_string.split(':')
        except ValueError:
            raise AuthenticationFailed('Invalid basic authentication credentials.')

        # Custom authentication logic here
        # For example, you can check if the user exists and verify the password
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user, None
            else:
                raise AuthenticationFailed('Invalid username or password.')
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid username or password.')
