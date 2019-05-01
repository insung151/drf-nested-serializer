import json

from django.test import TestCase, RequestFactory
from rest_framework import status

from drf_nested_serializer.tests.models import SimpleModel, O2ORelatedModel
from drf_nested_serializer.tests.views import FKCreateAPIView, M2MCreateAPIView, O2OCreateAPIView, O2OCreateAPIView2


class DRFNestedSerializerTests(TestCase):
    def setUp(self):
        super(DRFNestedSerializerTests, self).setUp()
        self.request = RequestFactory()

    def test_o2o_create(self):
        view = O2OCreateAPIView.as_view()
        data = json.dumps({"content": "test", "o2o_models": {"key": "1"}})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleModel.objects.count(), 1)
        simple_model = SimpleModel.objects.last()
        self.assertEqual(O2ORelatedModel.objects.filter(simple_model=simple_model).count(), 1)

    def test_fk_create(self):
        view = FKCreateAPIView.as_view()
        data = json.dumps({"content": "test", "fk_models": [{"key": "1"}, {"key": "2"}, {"key": "3"}]})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleModel.objects.count(), 1)
        self.assertEqual(
            SimpleModel.objects.get(pk=resp.data['id']).fk_models.count(), 3
        )

    def test_m2m_create(self):
        view = M2MCreateAPIView.as_view()
        data = json.dumps({"content": "test", "m2m_models": [{"key": "1"}, {"key": "2"}, {"key": "3"}]})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleModel.objects.count(), 1)
        self.assertEqual(
            SimpleModel.objects.get(pk=resp.data['id']).m2m_models.count(), 3
        )
