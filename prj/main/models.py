from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=300)
    katgorie = models.IntegerField(blank=True, null=True)