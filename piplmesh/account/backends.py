from django.contrib.auth.models import User as auth_user
from django.contrib.auth.backends import ModelBackend as auth_model_backend

class CaseInsensitiveModelBackend(auth_model_backend):
    """
    This backend uses case insensitive username authentication which is not supported by default
    """	
    def authenticate(self, username=None, password=None):
        try:
            user = auth_user.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except auth_user.DoesNotExist:
            return None