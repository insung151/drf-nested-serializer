from django.conf.urls import url

from .views import ReverseO2OCreateAPIView

urlpatterns = [
    url('', ReverseO2OCreateAPIView.as_view())
]