from tastypie import authorization as tastypie_authorization

class PostAuthorization(tastypie_authorization.Authorization):
    def is_authorized(self, request, object=None):
        try:
            obj = self.resource_meta.queryset[0]
        except (IndexError, TypeError):
            return True
        
        if obj.is_published:
            return True
        else:
            return obj.author == request.user