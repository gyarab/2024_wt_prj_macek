from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=300)
    katgorie = models.IntegerField(blank=True, null=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name