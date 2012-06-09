from mongoengine import queryset
from tastypie import authorization as tastypie_authorization

class PostAuthorization(tastypie_authorization.Authorization):
    def apply_limits(self, request, object_list):
        if request and hasattr(request, 'user'):
            if request.user.is_authenticated():
                object_list = object_list.filter((queryset.Q(author=request.user) & queryset.Q(is_published=False)) | queryset.Q(is_published=True))
                print object_list

        return object_list