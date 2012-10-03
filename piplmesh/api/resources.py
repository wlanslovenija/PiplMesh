from tastypie import authorization as tastypie_authorization, fields as tastypie_fields

from tastypie_mongoengine import fields as tastypie_mongoengine_fields, paginator, resources

from piplmesh.account import models as account_models
from piplmesh.api import authorization, fields, models as api_models, signals, tasks

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
    author = tastypie_mongoengine_fields.ReferenceField(to='piplmesh.api.resources.UserResource', attribute='author', null=False, full=True, readonly=True)

    def hydrate(self, bundle):
        bundle = super(AuthoredResource, self).hydrate(bundle)
        bundle.obj.author = bundle.request.user
        return bundle

class CommentResource(AuthoredResource):
    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(CommentResource, self).obj_create(bundle, request=request, **kwargs)

        # By default, comment author is subscribed to the post
        if bundle.obj.author not in self.instance.subscribers:
            self.instance.subscribers.append(bundle.obj.author)
            self.instance.save()

        signals.comment_created.send(sender=self, comment=bundle.obj, post=self.instance, request=request or bundle.request, bundle=bundle)

        # We process notifications asynchronously as it could
        # take long and we want REST request to finish quick
        tasks.process_notifications_on_new_comment.delay(bundle.obj.pk, self.instance.pk)

        return bundle

    class Meta:
        object_class = api_models.Comment
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        # TODO: Make proper authorization, current implementation is for development use only
        authorization = tastypie_authorization.Authorization()

class NotificationResource(resources.MongoEngineResource):
    post = tastypie_mongoengine_fields.ReferenceField(to='piplmesh.api.resources.PostResource', attribute='post', null=False, full=False)
    comment = fields.CustomReferenceField(to='piplmesh.api.resources.CommentResource', getter=lambda obj: obj.post.comments[obj.comment], setter=lambda obj: obj.pk, null=False, full=True)

    class Meta:
        queryset = api_models.Notification.objects.all()
        allowed_methods = ('get',)
        authorization = authorization.NotificationAuthorization()
        excludes = ('recipient',)

class ImageAttachmentResource(AuthoredResource):
    image_file = tastypie_mongoengine_fields.ReferenceField(to='piplmesh.api.resources.UploadedFileResource', attribute='image_file', null=False, full=True)
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
    """
    Query set is ordered by updated time for following reasons:
     * those who open web page anew will get posts in updated time order
     * others with already opened page will get updated posts again as they
       will request them based on ID of current newest post

    This is useful if we would like to show on the client side that post has been updated
    (but we do not necessary have to reorder them, this depends on the client code).
    """

    updated_time = tastypie_fields.DateTimeField(attribute='updated_time', null=False, readonly=True)
    comments = tastypie_mongoengine_fields.EmbeddedListField(of='piplmesh.api.resources.CommentResource', attribute='comments', default=lambda: [], null=True, full=False)
    attachments = tastypie_mongoengine_fields.EmbeddedListField(of='piplmesh.api.resources.AttachmentResource', attribute='attachments', default=lambda: [], null=True, full=True)

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(PostResource, self).obj_create(bundle, request=request, **kwargs)

        # By default, post author is subscribed to the post
        bundle.obj.subscribers.append(bundle.obj.author)
        bundle.obj.save()

        signals.post_created.send(sender=self, post=bundle.obj, request=request or bundle.request, bundle=bundle)

        return bundle

    class Meta:
        queryset = api_models.Post.objects.all().order_by('-updated_time')
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = authorization.PostAuthorization()
        paginator_class = paginator.Paginator
