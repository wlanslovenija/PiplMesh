import posixpath, time, urllib, uuid

from django import http
from django.core import exceptions
from django.core.files import storage, uploadedfile
from django.conf import settings
from django.utils import http as http_utils
from django.views import static

from mongoengine.django import storage as mongoengine_storage

class GridFSStorage(mongoengine_storage.GridFSStorage):
    """
    A storage backend to store files in GridFS, with additional
    support for UploadedFile, UUID filenames, and mimetype.
    """

    def _save(self, name, content):
        if not isinstance(uploadedfile.UploadedFile, content):
            return super(GridFSStorage, self)._save(name, content)

        doc = self.document()
        field = getattr(doc, self.field)

        field.new_file(filename=name, content_type=content.content_type)
        for chunk in content.chunks():
            field.write(chunk)
        field.close()

        doc.save()

        return name

    def get_available_name(self, name):
        # We ignore given name
        name = str(uuid.uuid4())

        while self.exists(name):
            name = str(uuid.uuid4())

        return name

    def created_time(self, name):
        doc = self._get_doc_with_name(name)
        if doc:
            return getattr(doc, self.field).upload_date
        else:
            raise ValueError("No such file or directory: '%s'" % name)

    def modified_time(self, name):
        # We assume GridFS files are immutable
        # (new version is done for changes)
        return self.created_time(name)

    def mimetype(self, name):
        doc = self._get_doc_with_name(name)
        if doc:
            return getattr(doc, self.field).content_type
        else:
            raise ValueError("No such file or directory: '%s'" % name)

def serve(request, path):
    """
    Serve files from default storage.

    To use, put a URL pattern such as::

        (r'^(?P<path>.*)$', 'piplmesh.utils.storage.serve')

    in your URLconf.
    """

    if not settings.DEBUG:
        raise exceptions.ImproperlyConfigured("The view can only be used in debug mode.")
    normalized_path = posixpath.normpath(urllib.unquote(path)).lstrip('/')

    if not storage.default_storage.exists(normalized_path):
        if path.endswith('/') or path == '':
            raise http.Http404("Directory indexes are not allowed here.")
        raise http.Http404("'%s' could not be found" % path)

    try:
        mimetype = storage.default_storage.mimetype(normalized_path) or 'application/octet-stream'
    except (NotImplementedError, AttributeError):
        mimetype = 'application/octet-stream'

    try:
        modified_time = time.mktime(storage.default_storage.modified_time(normalized_path).timetuple())
    except (NotImplementedError, AttributeError):
        modified_time = None

    size = storage.default_storage.size(normalized_path)

    if modified_time is not None and not static.was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), modified_time, size):
        return http.HttpResponseNotModified(mimetype=mimetype)

    f = storage.default_storage.open(normalized_path, 'rb')
    try:
        response = http.HttpResponse(f.read(), mimetype=mimetype)
    finally:
        f.close()

    response['Content-Length'] = size

    if modified_time is not None:
        response['Last-Modified'] = http_utils.http_date(modified_time)

    return response
