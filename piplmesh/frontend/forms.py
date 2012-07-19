from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
    """
    Class with contact form.
    """  
    subject = forms.CharField(label=_("Subject"))
    email = forms.EmailField(label=_("E-mail"))
    message = forms.CharField(widget=widgets.Textarea())