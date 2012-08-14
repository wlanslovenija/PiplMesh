from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

class ContactForm(forms.Form):
    """
    Class with the contact form.
    """  
    
    subject = forms.CharField(label=_("Subject"))
    email = forms.EmailField(label=_("Your e-mail address"))
    message = forms.CharField(widget=widgets.Textarea())
