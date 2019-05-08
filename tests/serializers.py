from drf_nested_serializer import NestedModelSerializer
from .models import SimpleModel, ForwardRelationModel


class ReverseO2OSerializer(NestedModelSerializer):
    class Meta:
        model = SimpleModel
        nested_fields = {'o2o_models': 'simple_model'}
        fields = '__all__'


class ReverseFKSerializer(NestedModelSerializer):
    class Meta:
        model = SimpleModel
        nested_fields = {'fk_models': 'simple_model'}
        fields = '__all__'


class ReverseM2MSerializer(NestedModelSerializer):
    class Meta:
        model = SimpleModel
        nested_fields = {'m2m_models': 'simple_model'}
        fields = '__all__'


class ForwardO2OSerializer(NestedModelSerializer):
    class Meta:
        model = ForwardRelationModel
        nested_fields = {'o2o': ' forward_relation_model'}
        fields = '__all__'


class ForwardFKSerializer(NestedModelSerializer):
    class Meta:
        model = ForwardRelationModel
        nested_fields = {'fk': ' forward_relation_model'}
        fields = '__all__'


class ForwardM2MSerializer(NestedModelSerializer):
    class Meta:
        model = ForwardRelationModel
        nested_fields = {'m2m': ' forward_relation_model'}
        fields = '__all__'
