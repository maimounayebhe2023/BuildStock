from rest_framework import serializers
from .models import Product, ProductCategory,ProductUnit


class ProductCategorySerializer(serializers.ModelSerializer):
    category_name= serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name',  'category_name',]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError('Un produit avec ce nom existe déjà')
        return value

class ProductUnitSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductUnit
        fields = ['id','product', 'product_name', 'unit_name',  'factor_to_base','is_base']

    def validate(self, data):
        if data.get('is_base'):
            qs = ProductUnit.objects.filter(
                product=data['product'],
                is_base=True
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
        return data

    def create(self, validated_data):
        if validated_data.get('is_base'):
            ProductUnit.objects.filter(
                product=validated_data['product'],
                is_base=True
            ).update(is_base=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('is_base'):
            ProductUnit.objects.filter(
                product=instance.product,
                is_base=True
            ).exclude(pk=instance.pk).update(is_base=False)
        return super().update(instance, validated_data)
