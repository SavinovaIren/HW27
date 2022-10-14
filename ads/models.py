from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=8, decimal_places=6)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50, default="member")
    age = models.PositiveIntegerField()
    location = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ad(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="ads")
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/', null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


