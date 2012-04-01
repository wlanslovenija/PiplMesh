from django.contrib.auth import models as auth_models
from django.db import models as django_models

from piplmesh.account import fields

class UserProfile(django_models.Model):
    """ 
    Class used for storing additional information about user.
    """

    user = django_models.OneToOneField(auth_models.User)

    # Custom fields
    birthdate = django_models.DateField(blank=True, null=True)
    gender = django_models.CharField(max_length=6, blank=True)
    facebook_id = django_models.BigIntegerField(verbose_name=u'Facebook ID', null=True, blank=True)
    token = django_models.CharField(max_length=150)
    language = fields.LanguageField(verbose_name=u'language')
    
    def __unicode__(self):
        return u'%s' % (self.user)
