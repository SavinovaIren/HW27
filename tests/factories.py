from datetime import date

import factory

from ads.models import User, Ad, Selection, Category


class UserFactory(factory.django.DjangoModelFactory):
    first_name = 'test'
    last_name ='test'
    username = factory.Faker('name')
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    role = 'admin'
    password = '123456'
    age = 36
    birth_date = factory.Faker('date_object')

    class Meta:
        model = User


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'test_cat_name'
    slug = 'test_cat_slug'


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = 'test_name_ad'
    author = factory.SubFactory(UserFactory)
    price = 100
    is_published = False
    category = factory.SubFactory(CategoryFactory)


class SelectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Selection

    name = 'test_name_selection'
    owner = factory.SubFactory(UserFactory)
    items = factory.RelatedFactoryList(AdFactory)


