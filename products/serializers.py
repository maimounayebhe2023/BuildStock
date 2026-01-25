from rest_framework import serializers
from .models import Product, ProductCategory, ProductUnit, Unit

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['uuid', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['uuid', 'name', 'description', 'is_active', 'stock_quantity', 'created_at', 'category', 'category_name']
        read_only_fields = ['uuid', 'stock_quantity', 'created_at']

    def validate_name(self, value):
        qs = Product.objects.filter(name=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A product with this name already exists.")
        return value


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['uuid', 'name', 'symbol']
        read_only_fields = ['uuid']


class ProductUnitSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    conversion_factor = serializers.DecimalField(max_digits=10, decimal_places=3, coerce_to_string=False)

    class Meta:
        model = ProductUnit
        fields = ['uuid', 'product', 'product_name', 'unit', 'unit_name', 'conversion_factor', 'is_base']

    def validate(self, data):
        if data.get('is_base'):
            qs = ProductUnit.objects.filter(product=data['product'], is_base=True)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("A base unit already exists for this product.")
        return data

    def create(self, validated_data):
        if validated_data.get('is_base'):
            ProductUnit.objects.filter(product=validated_data['product'], is_base=True).update(is_base=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('is_base'):
            ProductUnit.objects.filter(product=instance.product, is_base=True).exclude(pk=instance.pk).update(is_base=False)
        return super().update(instance, validated_data)