from django.conf import settings
from django.db.models import fields
from django.utils import translation

def get_initial_language(request=None):
    return settings.LANGUAGE_CODE

class LanguageField(fields.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 5)
        kwargs.setdefault('choices', settings.LANGUAGES)
        kwargs.setdefault('default', get_initial_language)
        
        super(fields.CharField, self).__init__(*args, **kwargs)
        
    def get_internal_type(self):
        return "CharField"