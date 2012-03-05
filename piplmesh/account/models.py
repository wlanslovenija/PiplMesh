from django.contrib.auth import models as auth_models
from django.db import models as django_models

class UserProfile(django_models.Model):
    """ 
	Class used for storing additional information about user
	"""
    user = django_models.OneToOneField(auth_models.User)

    # Custom fields
    gender = django_models.CharField(null=True, blank=True, max_length=1)
    birthdate = django_models.DateField(null=True, blank=True)
