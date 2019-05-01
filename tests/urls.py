from django.conf.urls import url

from .views import O2OCreateAPIView

urlpatterns = [
    url('', O2OCreateAPIView.as_view())
]