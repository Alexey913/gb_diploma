# Generated by Django 4.2.7 on 2023-12-06 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='phone',
            field=models.IntegerField(blank=True, verbose_name='Номер телефона'),
        ),
    ]
