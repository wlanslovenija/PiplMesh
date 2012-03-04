from django.db import models
from django.contrib.auth.models import User

#Storing additional information about users
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # Custom fields
    gender = models.BooleanField() #true=male, false=female
    birthdate = models.DateField()