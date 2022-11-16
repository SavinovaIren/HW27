from datetime import date

import factory
from faker import Factory as FakerFactory
faker = FakerFactory.create()

from ads.models import User, Ad, Selection, Category


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
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

    name = factory.Faker('name')
    slug = factory.LazyAttribute(lambda n: faker.sentence()[:10])


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = 'test_name_a'
    author = factory.SubFactory(UserFactory)
    price = 100
    is_published = False
    category = factory.SubFactory(CategoryFactory)


class SelectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Selection

    name = 'test_name_s'
    owner = factory.SubFactory(UserFactory)
    items = factory.RelatedFactoryList(AdFactory)


