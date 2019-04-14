import json

from django.test import TestCase, RequestFactory
from rest_framework import status

from drf_nested_serializer.tests.models import SimpleModel
from drf_nested_serializer.tests.views import SimpleModelCreateAPIView


class DRFNestedSerializerTests(TestCase):
    def setUp(self):
        super(DRFNestedSerializerTests, self).setUp()
        self.request = RequestFactory()

    def test_create(self):
        view = SimpleModelCreateAPIView.as_view()
        data = json.dumps(
            {
                "content":  "test",
                "related_models": [
                    {"key": "1"},
                    {"key": "2"},
                    {"key": "3"}
                ]
            }
        )
        resp = view(
            self.request.post(
                '',
                data,
                content_type='application/json'
            )
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleModel.objects.count(), 1)
        self.assertEqual(
            SimpleModel.objects.get(pk=resp.data['id']).related_models.count(), 3
        )
