from django.db import models

from user_app.models import User
from .common_data import GENDERS

class People(models.Model):

    class Meta:
        abstract = True

    surname = models.CharField(max_length=50, null=True, blank=True, verbose_name='Фамилия')
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, null=True, blank=True, verbose_name='Отчество')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=7, null=True, blank=True, choices=GENDERS, verbose_name='Пол')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
