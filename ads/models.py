from django.db import models

# Create your models here.
class Ads(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.FloatField(max_length=20)
    lang = models.FloatField(max_length=20)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
