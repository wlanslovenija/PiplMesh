from django.contrib.auth import backends, models as auth_models

class CaseInsensitiveModelBackend(backends.ModelBackend):
    """
    This backend uses case-insensitive username authentication which is not supported by default.
    """
    
    def authenticate(self, username=None, password=None):
        try:
            user = auth_models.User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except auth_models.User.DoesNotExist:
            return None