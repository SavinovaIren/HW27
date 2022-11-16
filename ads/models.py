from datetime import datetime, date, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

def check_email(value:str):
    if "rambler.ru" in value:
        raise ValidationError(
            '%(value)s is in the email',
            params={'value': value},
        )

def check_age(value: datetime):
    data = tuple([int(user) for user in value.rsplit("-")])
    birth_date = datetime(*data)
    age = (datetime.today() - birth_date) // timedelta(days=365.2425)
    if age < 9:
        raise ValidationError(
            '%(value)s is too small age',
            params={'value': value},
        )

def is_published(value):
    if value:
        raise ValidationError("is_published can't be True")
    return value



class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(5)])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name


class User(AbstractUser):
    USER = 'member'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    choices = [(USER, 'Пользователь'),
        (ADMIN, 'Админ'),
        (MODERATOR, 'Модератор'),]


    role = models.CharField(choices=choices, max_length=50, default="member")
    age = models.PositiveIntegerField()
    location = models.ManyToManyField(Location)
    email = models.CharField(max_length=100, unique=True, validators=[check_email])
    birth_date = models.DateField(validators=[check_age])

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ad(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="ads")
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(null=True)
    is_published = models.BooleanField(default=False,validators=[is_published])
    image = models.ImageField(upload_to='media/', null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

class Selection(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selections')
    name = models.CharField(max_length=200, unique=True)
    items = models.ManyToManyField(Ad)
    class Meta:
        verbose_name = 'Подборка объявлений'
        verbose_name_plural = 'Подборки объявлений'

    def __str__(self):
        return self.name
