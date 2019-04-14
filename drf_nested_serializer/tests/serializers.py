from drf_nested_serializer.serializers import NestedModelSerializer
from drf_nested_serializer.tests.models import SimpleModel


class SimpleModelSerializer(NestedModelSerializer):
    class Meta:
        model = SimpleModel
        nested_fields = {'related_models': 'simple_model'}
        fields = '__all__'
