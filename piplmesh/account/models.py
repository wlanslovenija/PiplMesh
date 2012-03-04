from django.db import models
from django.contrib.auth.models import User

#Storing additional information about users
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # Custom fields
    gender = models.CharField(null=True, blank=True, max_length=1)
    birthdate = models.DateField(null=True, blank=True)