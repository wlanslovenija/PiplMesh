from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _

from piplmesh import nodes

NO_MOCKING_ID = ''

class ContactForm(forms.Form):
    """
    Class with the contact form.
    """

    subject = forms.CharField(label=_("Subject"))
    email = forms.EmailField(label=_("Your e-mail address"))
    message = forms.CharField(widget=widgets.Textarea())

def location_choices():
    yield (NO_MOCKING_ID, _("Don't mock location"))
    for backend, node in nodes.get_all_nodes_with_backends():
        yield (nodes.get_full_node_id(backend.get_full_name(), node.id), node.name)

def initial_location(request):
    return request.node.get_full_node_id() if nodes.is_mocking(request) else NO_MOCKING_ID

class LocationsForm(forms.Form):
    location = forms.ChoiceField(choices=location_choices(), label=_("Location"), required=False)