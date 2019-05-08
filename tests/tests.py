import json

from django.test import TestCase, RequestFactory
from rest_framework import status

from .models import SimpleModel, O2ORelatedModel, ForwardRelationModel
from .views import ReverseFKCreateAPIView, ReverseM2MCreateAPIView, ReverseO2OCreateAPIView, ForwardO2OCreateAPIView, \
    ForwardFKCreateAPIView, ForwardM2MCreateAPIView


class DRFNestedSerializerTests(TestCase):
    def setUp(self):
        super(DRFNestedSerializerTests, self).setUp()
        self.request = RequestFactory()

    def test_reverse_o2o_create(self):
        view = ReverseO2OCreateAPIView.as_view()
        data = json.dumps({"content": "test", "o2o_models": {"key": "1"}})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleModel.objects.count(), 1)
        simple_model = SimpleModel.objects.last()
        self.assertEqual(O2ORelatedModel.objects.filter(simple_model=simple_model).count(), 1)

    def test_reverse_fk_create(self):
        view = ReverseFKCreateAPIView.as_view()
        data = json.dumps({"content": "test", "fk_models": [{"key": "1"}, {"key": "2"}, {"key": "3"}]})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleModel.objects.count(), 1)
        self.assertEqual(
            SimpleModel.objects.get(pk=resp.data['id']).fk_models.count(), 3
        )

    def test_reverse_m2m_create(self):
        view = ReverseM2MCreateAPIView.as_view()
        data = json.dumps({"content": "test", "m2m_models": [{"key": "1"}, {"key": "2"}, {"key": "3"}]})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleModel.objects.count(), 1)
        self.assertEqual(
            SimpleModel.objects.get(pk=resp.data['id']).m2m_models.count(), 3
        )

    def test_forward_o2o_create(self):
        view = ForwardO2OCreateAPIView.as_view()
        data = json.dumps({"content": "test", "o2o": {"key": "1"}})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ForwardRelationModel.objects.count(), 1)
        obj = ForwardRelationModel.objects.last()
        self.assertIsNotNone(obj.o2o)


    def test_forward_fk_create(self):
        view = ForwardFKCreateAPIView.as_view()
        data = json.dumps({"content": "test", "fk": {"key": "1"}})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ForwardRelationModel.objects.count(), 1)
        obj = ForwardRelationModel.objects.last()
        self.assertIsNotNone(obj.fk)

    def test_forward_m2m_create(self):
        view = ForwardM2MCreateAPIView.as_view()
        data = json.dumps({"content": "test", "m2m": [{"key": "1"}, {"key": "2"}, {"key": "3"}]})
        resp = view(self.request.post('', data, content_type='application/json'))
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ForwardRelationModel.objects.count(), 1)
        obj = ForwardRelationModel.objects.last()
        self.assertEqual(obj.m2m.count(), 3)
