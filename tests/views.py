from rest_framework.generics import CreateAPIView

from .models import SimpleModel
from .serializers import FKSerializer, M2MSerializer, O2OSerializer


class O2OCreateAPIView(CreateAPIView):
    serializer_class = O2OSerializer
    queryset = SimpleModel.objects.all()


class FKCreateAPIView(CreateAPIView):
    serializer_class = FKSerializer
    queryset = SimpleModel.objects.all()


class M2MCreateAPIView(CreateAPIView):
    serializer_class = M2MSerializer
    queryset = SimpleModel.objects.all()
