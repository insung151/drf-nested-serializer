from rest_framework.generics import CreateAPIView

from .models import SimpleModel, ForwardRelationModel
from .serializers import ReverseFKSerializer, ReverseM2MSerializer, ReverseO2OSerializer, ForwardO2OSerializer, \
    ForwardFKSerializer, ForwardM2MSerializer


class ReverseO2OCreateAPIView(CreateAPIView):
    serializer_class = ReverseO2OSerializer
    queryset = SimpleModel.objects.all()


class ReverseFKCreateAPIView(CreateAPIView):
    serializer_class = ReverseFKSerializer
    queryset = SimpleModel.objects.all()


class ReverseM2MCreateAPIView(CreateAPIView):
    serializer_class = ReverseM2MSerializer
    queryset = SimpleModel.objects.all()


class ForwardO2OCreateAPIView(CreateAPIView):
    serializer_class = ForwardO2OSerializer
    queryset = ForwardRelationModel.objects.all()


class ForwardFKCreateAPIView(CreateAPIView):
    serializer_class = ForwardFKSerializer
    queryset = ForwardRelationModel.objects.all()


class ForwardM2MCreateAPIView(CreateAPIView):
    serializer_class = ForwardM2MSerializer
    queryset = ForwardRelationModel.objects.all()
