from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from piplmesh import nodes

class ContactForm(forms.Form):
    """
    Class with the contact form.
    """  
    
    subject = forms.CharField(label=_("Subject"))
    email = forms.EmailField(label=_("Your e-mail address"))
    message = forms.CharField(widget=widgets.Textarea())

def location_choices():
    yield ('', _("Don't mock location"))
    for backend, node in nodes.get_all_nodes_with_backends():
        yield ('%s-%s' % (backend.get_full_name(), node.id), node.name)

class LocationsForm(forms.Form):
    locations = forms.ChoiceField(choices=location_choices(), label='', required=False)
