# Generated by Django 4.1.1 on 2022-10-10 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_location_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ads',
            options={'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Локация', 'verbose_name_plural': 'Локации'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]