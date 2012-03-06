from django.contrib.auth import models as auth_models
from django.db import models as django_models

class UserProfile(django_models.Model):
    """ 
    Class used for storing additional information about user
    """
    user = django_models.OneToOneField(auth_models.User)

    # Custom fields
    birthdate = django_models.DateField(null=True, blank=True)
    gender = django_models.CharField(max_length=6, blank=True)
    fid = django_models.BigIntegerField(verbose_name=u'Facebook ID')
    token = django_models.CharField(max_length=150)
    
    def __unicode__(self):
        return u'%s' % (self.user)
