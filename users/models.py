from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin' , 'Admin'),
        ('storekeeper' , 'Magasinier'),
        ('account', 'Comptable'),
    )
    role=models.CharField(max_length=15, choices=ROLE_CHOICES)
    phone=models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"{self.username} {self.role}"


