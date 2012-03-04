from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """ 
	Class used for storing additional information about user
	"""
    user = models.OneToOneField(User)

    # Custom fields
    gender = models.CharField(null=True, blank=True, max_length=1)
    birthdate = models.DateField(null=True, blank=True)
