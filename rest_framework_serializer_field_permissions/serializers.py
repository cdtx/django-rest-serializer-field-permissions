"""
Drop in serializer mixins.
"""
from .fields import PermissionMixin, class_substitution


class FieldPermissionSerializerMixin(object):
    """
    Mixin to your serializer class as follows:

        class PersonSerializer(FieldPermissionSerializerMixin, serializers.ModelSerializer):

            family_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
            given_names = fields.CharField(permission_classes=(IsAuthenticated(), ))
    """
    def build_field(self, field_name, info, model_class, nested_depth):
        # Let the original method determine the appropriate DRF field class
        ret = super(FieldPermissionSerializerMixin, self).build_field(field_name, info, model_class, nested_depth)
        # Substitute the class with our subclass's equivalent
        ret = (class_substitution.get(ret[0], ret[0]), ret[1])
        return ret

    @property
    def fields(self):
        """
        Supercedes drf's serializers.ModelSerializer's fields property
        :return: a set of permission-scrubbed fields
        """
        ret = super(FieldPermissionSerializerMixin, self).fields
        request = self.context.get("request")

        for field_name, field in ret.items():
            if hasattr(field, 'check_permission') and (not field.check_permission(request)):
                ret.pop(field_name)

        return ret
