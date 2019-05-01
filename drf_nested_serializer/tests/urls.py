from django.conf.urls import url

from drf_nested_serializer.tests.views import O2OCreateAPIView

urlpatterns = [
    url('', O2OCreateAPIView.as_view())
]