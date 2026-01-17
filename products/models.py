from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    """
    Represents a category of products
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Represents a product
    """
    category = models.ForeignKey(
        ProductCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="Category"
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name 


class ProductUnit(models.Model):
    """
    Represents different unit variations for a product
    e.g., 1 sac = 50 kg, 1 tonne = 1000 kg
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="units")
    unit_name = models.CharField(max_length=50)
    factor_to_base = models.FloatField(help_text="Number of base units this unit represents (e.g., 1 sac = 50 kg)")
    is_base = models.BooleanField(default=False, help_text="True if this is the base unit for the product") 

    def __str__(self):
        base = " (base)" if self.is_base else ""
        return f"{self.unit_name} of {self.product}{base}"

    

class ProductPrice(models.Model):
    """
    Represents the price of a product for a given unit
    Only one price per ProductUnit can be current at a time
    """
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True) 
    is_current = models.BooleanField(default=True, help_text="True if this price is the current price for the product unit")  

    def __str__(self):
        status = "Current" if self.is_current else "Expired"
        return f"{self.product_unit} - {self.price} GNF ({status})"