from django.db import transaction, router
from django.db.models.fields.related_descriptors import ForwardOneToOneDescriptor
from rest_framework import serializers
from rest_framework.serializers import ListSerializer, ModelSerializer


def serializer_factory(model, serializer=serializers.ModelSerializer):
    meta_class = type('Meta', (), dict(model=model, fields='__all__'))
    attrs = {'Meta': meta_class}
    return type(model.__class__.__name__ + 'Serializer', (serializer,), attrs)


class NestedModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(NestedModelSerializer, self).__init__(*args, **kwargs)
        self.forward_fields, self.reverse_fields = [], []
        for field_name in self.Meta.nested_fields:
            if field_name in self.Meta.model._meta._forward_fields_map:
                self.forward_fields.append(field_name)
            else:
                self.reverse_fields.append(field_name)

    def _pop_reverse_fields(self):
        for field_name in self.reverse_fields:
            nested_serializer = self.fields[field_name]
            if isinstance(nested_serializer, ListSerializer):
                nested_serializer = nested_serializer.child
            nested_serializer._writable_fields = [
                nested_field for nested_field_name, nested_field in nested_serializer.fields.items()
                if not nested_field.read_only and nested_field_name != self.Meta.nested_fields[field_name]
            ]

    def _insert_reverse_fields(self):
        for field_name in self.reverse_fields:
            nested_serializer = self.fields[field_name]
            if isinstance(nested_serializer, ListSerializer):
                nested_serializer = nested_serializer.child
            if not isinstance(getattr(self.Meta.model, field_name), ForwardOneToOneDescriptor):
                nested_serializer._writable_fields.append(
                    nested_serializer.fields[self.Meta.nested_fields[field_name]]
                )

    def is_valid(self, raise_exception=False):
        self._pop_reverse_fields()
        is_valid = super(NestedModelSerializer, self).is_valid(raise_exception)
        self._insert_reverse_fields()
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

            if field_name not in self._declared_fields:
                related_field = self.Meta.model._meta.get_field(field_name)
                related_model = related_field.related_model
                if field_name in self.forward_fields:
                    many = related_field.many_to_many
                else:
                    many = not related_field.one_to_one
                fields[field_name] = serializer_factory(model=related_model)(many=many, required=False)

            assert isinstance(fields[field_name], ListSerializer) \
                   or isinstance(fields[field_name], ModelSerializer), (
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
                validated_data.pop(nested_field_name)
                nested_fields[nested_field_name] = self.initial_data[nested_field_name]

        many_to_many = {}
        for field_name in self.forward_fields:
            serializer = self.fields[field_name]
            serializer.initial_data = nested_fields.pop(field_name)
            serializer.is_valid(raise_exception=True)
            if self.Meta.model._meta.get_field(field_name).many_to_many:
                many_to_many[field_name] = serializer.save()
            else:
                validated_data[field_name] = serializer.save()

        instance = super(NestedModelSerializer, self).create(validated_data)

        for field_name, field in many_to_many.items():
            getattr(instance, field_name).add(*field)

        # Create nested objects
        for nested_field_name, nested_field_data in nested_fields.items():
            related_field = self.Meta.model._meta.get_field(nested_field_name)
            many = not related_field.one_to_one
            is_m2m = related_field.many_to_many
            if many:
                for data in nested_field_data:
                    if is_m2m:
                        data.update({self.Meta.nested_fields[nested_field_name]: [instance.pk]})
                    else:
                        data.update({self.Meta.nested_fields[nested_field_name]: instance.pk})
            else:
                nested_field_data.update({self.Meta.nested_fields[nested_field_name]: instance.pk})
        for field_name, field in nested_fields.items():
            serializer = self.fields[field_name]
            serializer.initial_data = nested_fields[field_name]
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return instance
