from django.db import models

# Create your models here.
class Ads(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)

class Category(models.Model):
    name = models.CharField(max_length=200)