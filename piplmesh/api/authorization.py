from mongoengine import queryset
from tastypie import authorization as tastypie_authorization

class PostAuthorization(tastypie_authorization.Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            object_list = object_list.filter(queryset.Q(author=request.user) | queryset.Q(is_published=True))
        else:
            object_list = object_list.filter(is_published=True)

        return object_list

class NotificationAuthorization(tastypie_authorization.Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            return object_list.filter(recipient=request.user)
        else:
            # TODO: Should be in fact empty queryset, https://github.com/MongoEngine/mongoengine/issues/127
            return []
