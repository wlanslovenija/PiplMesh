from django import forms
from django.views import generic as generic_views
from django.utils.translation import ugettext_lazy as _

class UploadForm(forms.Form):
    file = forms.FileField(label=_("File"))

class UploadFormView(generic_views.TemplateView):
    template_name = 'debug/uploadform.html'

    def get_context_data(self, **kwargs):
        context = super(UploadFormView, self).get_context_data(**kwargs)
        context.update({
            'form': UploadForm(),
        })
        return context
