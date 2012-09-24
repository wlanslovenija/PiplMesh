from tastypie_mongoengine import fields

class CustomReferenceField(fields.ReferenceField):
    """
    Reference field which allows custom getter to access attribute.
    """

    def __init__(self, attribute_getter, target_attribute, *args, **kwargs):
        super(CustomReferenceField, self).__init__(attribute=target_attribute, *args, **kwargs)

        self.attribute_getter = attribute_getter

    def dehydrate(self, bundle):
        setattr(bundle.obj, self.attribute, self.attribute_getter(bundle.obj))
        return super(CustomReferenceField, self).dehydrate(bundle)
