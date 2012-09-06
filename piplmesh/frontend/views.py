import smtplib

from django import dispatch, http, template
from django.conf import settings
from django.contrib import messages
from django.core import mail, urlresolvers
from django.core.files import storage
from django.utils.translation import ugettext_lazy as _
from django.views import generic as generic_views

from tastypie import http as tastypie_http
from tastypie.utils import formatting

from mongogeneric import detail

from pushserver.utils import updates

from piplmesh.account import models as account_models
from piplmesh.api import models as api_models, resources, signals
from piplmesh.frontend import forms

HOME_CHANNEL_ID = 'home'

class HomeView(generic_views.TemplateView):
    template_name = 'home.html'

# TODO: Get HTML5 geolocation data and store it into request session
class OutsideView(generic_views.TemplateView):
    template_name = 'outside.html'

class SearchView(generic_views.TemplateView):
    template_name = 'search.html'

class AboutView(generic_views.TemplateView):
    template_name = 'about.html'
      
class ContactView(generic_views.FormView):
    """
    This view checks if all contact data are valid and then sends e-mail to site managers.
    
    User is redirected back to the contact page.
    """
    
    template_name = 'contact.html'
    success_url = urlresolvers.reverse_lazy('contact')
    form_class = forms.ContactForm

    def form_valid(self, form):
        mail.mail_managers(form.cleaned_data['subject'], form.cleaned_data['message'], form.cleaned_data['email'])
        messages.success(self.request, _("Thank you. Your message has been successfully sent."))
        return super(ContactView, self).form_valid(form)

class UserView(detail.DetailView):
    """
    This view checks if user exist in database and returns his user page (profile).
    """

    template_name = 'user/user.html'
    document = account_models.User
    slug_field = 'username'
    slug_url_kwarg = 'username'

def upload_view(request):
    if request.method != 'POST':
        return http.HttpResponseBadRequest()

    resource = resources.UploadedFileResource()

    # TODO: Provide some user feedback while uploading

    uploaded_files = []
    for field, files in request.FILES.iterlists():
        for file in files:
            # We let storage decide a name
            filename = storage.default_storage.save('', file)

            uploaded_file = api_models.UploadedFile()
            uploaded_file.author = request.user
            uploaded_file.filename = filename
            uploaded_file.content_type = file.content_type
            uploaded_file.save()

            uploaded_files.append({
                'filename': filename,
                'resource_uri': resource.get_resource_uri(uploaded_file)
            })

    # TODO: Create background task to process uploaded file (check content type (both in GridFS file and UploadedFile document), resize images)

    return resource.create_response(request, uploaded_files, response_class=tastypie_http.HttpAccepted)

def forbidden_view(request, reason=''):
    """
    Displays 403 forbidden page. For example, when request fails CSRF protection.
    """

    from django.middleware import csrf
    t = template.loader.get_template('403.html')
    return http.HttpResponseForbidden(t.render(template.RequestContext(request, {
        'DEBUG': settings.DEBUG,
        'reason': reason,
        'no_referer': reason == csrf.REASON_NO_REFERER,
    })))

@dispatch.receiver(signals.post_created)
def send_update_on_new_post(sender, post, request, bundle, **kwargs):
    """
    Sends update to push server when a new post is created.
    """
    if post.is_published:
        output_bundle = sender.full_dehydrate(bundle)
        output_bundle = sender.alter_detail_data_to_serialize(request, output_bundle)

        serialized = sender.serialize(request, {
            'type': 'post_new',
            'post': output_bundle.data,
        }, 'application/json')

        updates.send_update(HOME_CHANNEL_ID, serialized, True)
