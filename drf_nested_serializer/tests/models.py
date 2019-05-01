from django.db import models


class SimpleModel(models.Model):
    content = models.CharField(max_length=100)
    key = models.OneToOneField(
        'KeyModel',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='simple_model'
    )


class O2ORelatedModel(models.Model):
    simple_model = models.OneToOneField(
        SimpleModel,
        related_name='o2o_models',
        on_delete=models.CASCADE,
    )
    key = models.CharField(max_length=100)


class FKRelatedModel(models.Model):
    simple_model = models.ForeignKey(
        SimpleModel,
        related_name='fk_models',
        on_delete=models.CASCADE
    )
    key = models.CharField(max_length=100)


class M2MRelatedModel(models.Model):
    simple_model = models.ManyToManyField(
        SimpleModel,
        related_name='m2m_models'
    )
    key = models.CharField(max_length=100)


class KeyModel(models.Model):
    key = models.CharField(max_length=100)
