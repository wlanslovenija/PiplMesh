import datetime

from tastypie import authorization, fields as tastypie_fields

from tastypie_mongoengine import fields, resources

from piplmesh.account import models as account_models
from piplmesh.api import models as api_models

class UserResource(resources.MongoEngineResource):
    class Meta:
        queryset = account_models.User.objects.all()
        fields = ('username', 'is_online')
        allowed_methods = ()

class CommentResource(resources.MongoEngineResource):
    created_time = tastypie_fields.DateTimeField(default=lambda: datetime.datetime.now(), null=False, readonly=True)
    author = fields.ReferenceField(to='piplmesh.api.resources.UserResource', attribute='author', null=False, full=True, readonly=True)

    class Meta:
        object_class = api_models.Comment
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        # TODO: Make proper authorization, current implementation is for development use only
        authorization = authorization.Authorization()

class ImageAttachmentResource(resources.MongoEngineResource):
    created_time = tastypie_fields.DateTimeField(default=lambda: datetime.datetime.now(), null=False, readonly=True)
    author = fields.ReferenceField(to='piplmesh.api.resources.UserResource', attribute='author', null=False, full=True, readonly=True)

    # This field is not required, but we still do not want null value, but empty string
    image_description = tastypie_fields.CharField(default='', null=False)

    class Meta:
        object_class = api_models.ImageAttachment

class LinkAttachmentResource(resources.MongoEngineResource):
    created_time = tastypie_fields.DateTimeField(default=lambda: datetime.datetime.now(), null=False, readonly=True)
    author = fields.ReferenceField(to='piplmesh.api.resources.UserResource', attribute='author', null=False, full=True, readonly=True)

    # These fields are not required, but we still do not want null values, but empty strings
    link_caption = tastypie_fields.CharField(default='', null=False)
    link_description = tastypie_fields.CharField(default='', null=False)

    class Meta:
        object_class = api_models.LinkAttachment

class AttachmentResource(resources.MongoEngineResource):
    created_time = tastypie_fields.DateTimeField(default=lambda: datetime.datetime.now(), null=False, readonly=True)
    author = fields.ReferenceField(to='piplmesh.api.resources.UserResource', attribute='author', null=False, full=True, readonly=True)

    class Meta:
        object_class = api_models.Attachment
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        # TODO: Make proper authorization, current implementation is for development use only
        authorization = authorization.Authorization()

        polymorphic = {
            'image': ImageAttachmentResource,
            'link': LinkAttachmentResource,
        }

class PostResource(resources.MongoEngineResource):
    created_time = tastypie_fields.DateTimeField(default=lambda: datetime.datetime.now(), null=False, readonly=True)
    updated_time = tastypie_fields.DateTimeField(null=False, readonly=True)
    author = fields.ReferenceField(to='piplmesh.api.resources.UserResource', attribute='author', null=False, full=True, readonly=True)

    # These fields are not required, but we still do not want null values, but empty lists
    comments = fields.EmbeddedListField(of='piplmesh.api.resources.CommentResource', attribute='comments', default=lambda: [], null=False, full=False)
    attachments = fields.EmbeddedListField(of='piplmesh.api.resources.AttachmentResource', attribute='attachments', default=lambda: [], null=False, full=True)

    class Meta:
        queryset = api_models.Post.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        # TODO: Make proper authorization, current implementation is for development use only
        authorization = authorization.Authorization()
