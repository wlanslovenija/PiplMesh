from tastypie import authorization as tastypie_authorization

class PiplMeshAuthorization(tastypie_authorization.Authorization):
    def is_authorized(self, request, object=None):
        try:
            obj = self.resource_meta.queryset[0]
        except (IndexError, TypeError):
            return True
        
        return True if obj.is_published else obj.author == request.user