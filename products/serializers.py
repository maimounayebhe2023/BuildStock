from rest_framework import serializers
from .models import Product, ProductCategory


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