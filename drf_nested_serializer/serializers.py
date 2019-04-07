from django.db import transaction, router
from rest_framework import serializers
from rest_framework.serializers import ListSerializer


def serializer_factory(model, serializer=serializers.ModelSerializer):
    meta_class = type('Meta', (), dict(model=model, fields='__all__'))
    attrs = {'Meta': meta_class}
    return type(model.__class__.__name__ + 'Serializer', (serializer,), attrs)

class NestedModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(NestedModelSerializer, self).__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        # remove nested fields for validation
        for field_name, related_name in self.Meta.nested_fields.items():
            nested_serializer = self.fields[field_name]
            nested_serializer.child._writable_fields = [
                nested_field for nested_field_name, nested_field in nested_serializer.child.fields.items()
                if not nested_field.read_only and nested_field_name != related_name
            ]

        is_valid = super(NestedModelSerializer, self).is_valid(raise_exception)

        for field_name, related_name in self.Meta.nested_fields.items():
            nested_serializer = self.fields[field_name]
            nested_serializer.child._writable_fields.append(
                nested_serializer.child.fields[self.Meta.nested_fields[field_name]]
            )
        return is_valid

    def get_field_names(self, declared_fields, info):
        field_names = super(NestedModelSerializer, self).get_field_names(declared_fields, info)

        for field_name in self.Meta.nested_fields:
            if field_name not in field_names:
                field_names.append(field_name)
        return field_names

    def get_fields(self):
        fields = super(NestedModelSerializer, self).get_fields()

        assert hasattr(self.Meta, 'nested_fields'), (
            'Class {serializer_class} missing "Meta.nested_fields" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )

        for field_name in self.Meta.nested_fields:
            assert (field_name in fields), (
                "{field_name} must be included in fields option ".format(
                    field_name=field_name
                )
            )

            if field_name not in self._declared_fields and \
                    not isinstance(fields[field_name], ListSerializer):
                related_model =  getattr(self.Meta.model, field_name).rel.related_model
                fields[field_name] = serializer_factory(model=related_model)(many=True, required=False)

            assert isinstance(fields[field_name], ListSerializer), (
                "{field_name} must be a 'ListSerializer' instance".format(
                    field_name=field_name
                )
            )

        return fields

    def create(self, validated_data):
        with transaction.atomic(using=router.db_for_write(self.Meta.model)):
            return self._create(validated_data)

    def _create(self, validated_data):
        # Remove nested serializer field
        nested_fields = {}
        for nested_field_name in self.Meta.nested_fields:
            if nested_field_name in validated_data:
                nested_fields[nested_field_name] = validated_data.pop(nested_field_name)

        instance = super(NestedModelSerializer, self).create(validated_data)

        # Create nested objects
        for nested_field_name, nested_field_data in nested_fields.items():
            for data in nested_field_data:
                data.update({self.Meta.nested_fields[nested_field_name]: instance.pk})
        for field_name, field in nested_fields.items():
            serializer = self.fields[field_name]
            serializer.initial_data = nested_fields[field_name]
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return instance
