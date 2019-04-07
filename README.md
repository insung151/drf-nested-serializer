# DRF Nested Serializer
Nested Serializer support for Django Rest Framework.

## Example
```python
class Goods(models.Model):
    name = models.CharField(max_length=10)
    category = models.CharField(max_length=20)

class GoodsImage(models.Model):
    goods = models.ForeignKey(
        Goods,
        related_name='goods_images',
        on_delete=models.CASCADE
    )
    image_key = models.CharField(max_length=10)
    
    

class GoodsSerializer(NestedModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'
        nested_fields = {'goods_images': 'goods'} # {related_name: field_name}
```

The above will allow to create the following queries


```
POST
{
    "name": "string",
    "category: "string",
    "goods_images": [
        {"image_key": "string"},
        {"image_key": "string"},
        {"image_key": "string"}
    ]
}
```