from django.conf.urls import url

from drf_nested_serializer.tests.views import SimpleModelCreateAPIView

urlpatterns = [
    url('', SimpleModelCreateAPIView.as_view())
]