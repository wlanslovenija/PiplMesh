from tastypie_mongoengine import fields

class CustomReferenceField(fields.ReferenceField):
    """
    Reference field which allows custom getter to access attribute.
    """

    def __init__(self, getter, setter, *args, **kwargs):
        super(CustomReferenceField, self).__init__(attribute=None, *args, **kwargs)

        self._getter = getter
        self._setter = setter

    def dehydrate(self, bundle):
        self.attribute = '_temp_proxy'
        setattr(bundle.obj, self.attribute, self._getter(bundle.obj))
        try:
            return super(CustomReferenceField, self).dehydrate(bundle)
        finally:
            delattr(bundle.obj, self.attribute)
            self.attribute = None

    def hydrate(self, bundle):
        value = super(CustomReferenceField, self).hydrate(bundle)

        if value is None:
            return value

        return self._setter(value)
