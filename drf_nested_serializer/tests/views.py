from rest_framework.generics import CreateAPIView

from drf_nested_serializer.tests.models import SimpleModel
from drf_nested_serializer.tests.serializers import SimpleModelSerializer


class SimpleModelCreateAPIView(CreateAPIView):
    serializer_class = SimpleModelSerializer
    queryset = SimpleModel.objects.all()
