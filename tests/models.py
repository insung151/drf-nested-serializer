from django.db import models


class SimpleModel(models.Model):
    content = models.CharField(max_length=100)


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


class ForwardRelationModel(models.Model):
    content = models.CharField(max_length=100)
    o2o = models.OneToOneField(
        'O2OModel',
        on_delete=models.CASCADE,
        related_name='forward_relation_model',
        blank=True,
        null=True
    )
    fk = models.ForeignKey(
        'FKModel',
        on_delete=models.CASCADE,
        related_name='forward_relation_model',
        blank=True,
        null=True
    )
    m2m = models.ManyToManyField(
        'M2MModel',
        related_name='forward_relation_model',
        blank=True,
    )


class O2OModel(models.Model):
    key = models.CharField(max_length=100)


class FKModel(models.Model):
    key = models.CharField(max_length=100)


class M2MModel(models.Model):
    key = models.CharField(max_length=100)
