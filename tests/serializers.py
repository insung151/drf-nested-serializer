from drf_nested_serializer import NestedModelSerializer
from .models import SimpleModel


class O2OSerializer(NestedModelSerializer):
    class Meta:
        model = SimpleModel
        nested_fields = {'o2o_models': 'simple_model'}
        fields = '__all__'


class FKSerializer(NestedModelSerializer):
    class Meta:
        model = SimpleModel
        nested_fields = {'fk_models': 'simple_model'}
        fields = '__all__'


class M2MSerializer(NestedModelSerializer):
    class Meta:
        model = SimpleModel
        nested_fields = {'m2m_models': 'simple_model'}
        fields = '__all__'
