from rest_framework import serializers
from .models import Product, ProductCategory,ProductUnit


class ProductCategorySerializer(serializers.ModelSerializer):
    category_name= serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'category', 'category_name',]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError('Un produit avec ce nom existe déjà')
        return value


class ProductUnitSerializer(serializers.ModelSerializer):
    product_name= serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model=ProductUnit
        fields= ['product', 'product_name', 'id', 'unit_name','factor_to_base','is_base' ]
      
    def validate(self, data):
        if data.get('is_base') and ProductUnit.objects.filter(
            product=data['product'],
            is_base=True
        ).exists():
            raise serializers.ValidationError(
                "Ce produit a déjà une unité de base."
            )
        return data
