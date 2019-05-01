from rest_framework.generics import CreateAPIView

from drf_nested_serializer.tests.models import SimpleModel
from drf_nested_serializer.tests.serializers import FKSerializer, M2MSerializer, O2OSerializer, O2OSerializer2


class O2OCreateAPIView(CreateAPIView):
    serializer_class = O2OSerializer
    queryset = SimpleModel.objects.all()


class O2OCreateAPIView2(CreateAPIView):
    serializer_class = O2OSerializer2
    queryset = SimpleModel.objects.all()


class FKCreateAPIView(CreateAPIView):
    serializer_class = FKSerializer
    queryset = SimpleModel.objects.all()


class M2MCreateAPIView(CreateAPIView):
    serializer_class = M2MSerializer
    queryset = SimpleModel.objects.all()
