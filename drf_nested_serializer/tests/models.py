from django.db import models


class SimpleModel(models.Model):
    content = models.CharField(max_length=100)


class RelatedModel(models.Model):
    simple_model = models.ForeignKey(
        SimpleModel,
        related_name='related_models',
        on_delete=models.CASCADE
    )
    key = models.CharField(max_length=100)
