import mongoengine

from django.conf import settings

def get_initial_language(request=None):
    return settings.LANGUAGE_CODE

class LanguageField(mongoengine.StringField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 5)
        kwargs.setdefault('choices', settings.LANGUAGES)
        kwargs.setdefault('default', get_initial_language)
        
        super(LanguageField, self).__init__(*args, **kwargs)
        
    def get_internal_type(self):
        return "StringField"