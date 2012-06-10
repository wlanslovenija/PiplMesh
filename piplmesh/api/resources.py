from tastypie import authorization as tastypie_authorization, fields as tastypie_fields

from tastypie_mongoengine import fields, resources

from piplmesh.account import models as account_models
from piplmesh.api import authorization, models as api_models

class UserResource(resources.MongoEngineResource):
    class Meta:
        queryset = account_models.User.objects.all()
        fields = ('username', 'is_online')
        allowed_methods = ()

class UploadedFileResource(resources.MongoEngineResource):
    class Meta:
        queryset = api_models.UploadedFile.objects.all()
        allowed_methods = ()

class AuthoredResource(resources.MongoEngineResource):
    created_time = tastypie_fields.DateTimeField(attribute='created_time', null=False, readonly=True)
    author = fields.ReferenceField(to='piplmesh.api.resources.UserResource', attribute='author', null=False, full=True, readonly=True)

    def hydrate(self, bundle):
        bundle = super(AuthoredResource, self).hydrate(bundle)
        bundle.obj.author = bundle.request.user
        return bundle

class CommentResource(AuthoredResource):
    class Meta:
        object_class = api_models.Comment
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        # TODO: Make proper authorization, current implementation is for development use only
        authorization = tastypie_authorization.Authorization()

class ImageAttachmentResource(AuthoredResource):
    image_file = fields.ReferenceField(to='piplmesh.api.resources.UploadedFileResource', attribute='image_file', null=False, full=True)
    image_description = tastypie_fields.CharField(attribute='image_description', default='', null=False, blank=True)

    class Meta:
        object_class = api_models.ImageAttachment

class LinkAttachmentResource(AuthoredResource):
    link_caption = tastypie_fields.CharField(attribute='link_caption', default='', null=False, blank=True)
    link_description = tastypie_fields.CharField(attribute='link_description', default='', null=False, blank=True)

    class Meta:
        object_class = api_models.LinkAttachment

class AttachmentResource(AuthoredResource):
    class Meta:
        object_class = api_models.Attachment
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        # TODO: Make proper authorization, current implementation is for development use only
        authorization = tastypie_authorization.Authorization()

        polymorphic = {
            'image': ImageAttachmentResource,
            'link': LinkAttachmentResource,
        }

class PostResource(AuthoredResource):
    updated_time = tastypie_fields.DateTimeField(attribute='updated_time', null=False, readonly=True)

    comments = fields.EmbeddedListField(of='piplmesh.api.resources.CommentResource', attribute='comments', default=lambda: [], null=True, full=False)
    attachments = fields.EmbeddedListField(of='piplmesh.api.resources.AttachmentResource', attribute='attachments', default=lambda: [], null=True, full=True)

    class Meta:
        queryset = api_models.Post.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        # TODO: Make proper authorization, current implementation is for development use only
        authorization = authorization.PostAuthorization()
