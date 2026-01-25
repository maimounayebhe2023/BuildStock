from django.db import models
import uuid

# Create your models here.

class ProductCategory(models.Model):
    """
    Represents a category of products
    """

    uuid = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    unique=True
    )    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Represents a product
    """

    uuid = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    unique=True
    )

    category = models.ForeignKey(
    'ProductCategory',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='products'
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
     return self.name


class Unit(models.Model):
    """
    Represents a unit of measurement for products, e.g., piece, bag, carton
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"



class ProductUnit(models.Model):
    """
    Represents different unit variations for a product
    e.g., 1 sac = 50 kg, 1 tonne = 1000 kg
    """

    uuid = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    unique=True
    )
    product = models.ForeignKey('Product', on_delete=models.CASCADE,  related_name='units')
    unit = models.ForeignKey('Unit',  on_delete=models.CASCADE, related_name='product_units' )
    is_base = models.BooleanField( default=False, help_text="Check if this is the product's main/base unit")
    conversion_factor = models.FloatField( default=1.0, help_text="Number of base units corresponding to this unit")

    class Meta:
        unique_together = ('product', 'unit')
   

    def __str__(self):
        base = " (Base)" if self.is_base else ""
        return f"{self.product.name} - {self.unit.name}{base}"
    
    