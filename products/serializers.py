from django.db import transaction
from rest_framework import serializers
from .models import Product, ProductCategory, ProductUnit, Unit

# --- Product Category ---
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['uuid', 'name', 'description']


# --- Unit ---
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['uuid', 'name', 'symbol']
        read_only_fields = ['uuid']


# --- Product ---
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    base_unit_id = serializers.PrimaryKeyRelatedField(
        queryset=Unit.objects.all(),
        write_only=True
    )

    secondary_units = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True
    )

    base_unit = serializers.SerializerMethodField(read_only=True)
    secondary_units_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'uuid', 'name', 'description', 'is_active',
            'category', 'category_name',
            'base_unit_id', 'secondary_units',
            'base_unit', 'secondary_units_details'
        ]
        read_only_fields = ['uuid', 'base_unit', 'secondary_units_details']

    # --- Validation ---
    def validate(self, attrs):
        base_unit = attrs['base_unit_id']
        secondary_units = attrs.get('secondary_units', [])
        secondary_unit_ids = [u['unit_id'] for u in secondary_units]

        if base_unit.id in secondary_unit_ids:
            raise serializers.ValidationError(
                "Base unit cannot be included in secondary units."
            )
        if len(secondary_unit_ids) != len(set(secondary_unit_ids)):
            raise serializers.ValidationError(
                "Duplicate units in secondary units."
            )
        return attrs

    # --- Create Product ---
    def create(self, validated_data):
        base_unit = validated_data.pop('base_unit_id')
        secondary_units = validated_data.pop('secondary_units', [])

        product = Product.objects.create(**validated_data)

        # Base unit
        ProductUnit.objects.create(
            product=product,
            unit=base_unit,
            is_base=True,
            conversion_factor=1
        )

        # Secondary units
        for su in secondary_units:
            ProductUnit.objects.create(
                product=product,
                unit_id=su['unit_id'],
                conversion_factor=su.get('conversion_factor', 1),
                is_base=False
            )

        return product

    # --- SerializerMethodFields ---
    def get_base_unit(self, obj):
        pu = obj.units.filter(is_base=True).first()
        if pu:
            return {"id": pu.unit.id, "name": pu.unit.name, "symbol": pu.unit.symbol}
        return None

    def get_secondary_units_details(self, obj):
        return [
            {
                "id": pu.unit.id,
                "name": pu.unit.name,
                "symbol": pu.unit.symbol,
                "conversion_factor": pu.conversion_factor
            }
            for pu in obj.units.filter(is_base=False)
        ]

    # --- Update Product ---
    @transaction.atomic
    def update(self, instance, validated_data):
        base_unit = validated_data.pop('base_unit_id', None)
        secondary_units = validated_data.pop('secondary_units', None)

        # Update product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if base_unit:
            ProductUnit.objects.filter(product=instance, is_base=True).update(is_base=False)
            ProductUnit.objects.update_or_create(
                product=instance,
                unit=base_unit,
                defaults={'is_base': True, 'conversion_factor': 1}
            )

        # --- Sync secondary units ---
        if secondary_units is not None:
            existing_units = {pu.unit_id: pu for pu in instance.units.filter(is_base=False)}
            incoming_ids = []

            for su in secondary_units:
                unit_id = su['unit_id']
                incoming_ids.append(unit_id)
                ProductUnit.objects.update_or_create(
                    product=instance,
                    unit_id=unit_id,
                    defaults={'conversion_factor': su.get('conversion_factor', 1), 'is_base': False}
                )

            for unit_id, pu in existing_units.items():
                if unit_id not in incoming_ids:
                    pu.delete()

        return instance