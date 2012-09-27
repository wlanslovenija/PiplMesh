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
    yield ('None', _("Don't mock location"))
    for backend, node in nodes.get_all_nodes_with_backends():
        yield (nodes.get_full_node_id(backend.get_full_name(), node.id), node.name)

def initial_location(request):
    node_id = request.session.get(nodes.SESSION_KEY, None)
    backend_name = request.session.get(nodes.BACKEND_SESSION_KEY, None)
    return nodes.get_full_node_id(backend_name, node_id) if nodes.is_mocking(request) else 'None'

class LocationsForm(forms.Form):
    location = forms.ChoiceField(choices=location_choices(), label=_("Location"), required=True)
