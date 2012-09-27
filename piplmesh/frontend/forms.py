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

class LocationsForm(forms.Form):
    locationChoices = [("%s_%s" % (backend.get_full_name(), node.id), node.name) for backend, node in nodes.get_all_nodes_with_backends()]
    locationChoices.insert(0, ('-1', _("Don't mock location")))
    locations = forms.ChoiceField(choices=locationChoices, label='', required=False)
