from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """ 
	Class used for storing additional information about user
	"""
    user = models.OneToOneField(User)

    # Custom fields
    gender = models.BooleanField() #true=male, false=female
    birthdate = models.DateField()