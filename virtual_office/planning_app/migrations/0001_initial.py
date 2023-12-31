# Generated by Django 4.2.7 on 2023-12-07 12:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Напоминание', max_length=20, verbose_name='Заголовок')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('time', models.TimeField(default=django.utils.timezone.now, verbose_name='Время')),
                ('all_day', models.BooleanField(default=False, verbose_name='Весь день')),
                ('repeat', models.CharField(choices=[('Каждую неделю', 'Каждую неделю'), ('Каждый год', 'Каждый год'), ('Каждый день', 'Каждый день'), ('Каждый месяц', 'Каждый месяц'), ('Никогда', 'Никогда')], default='Никогда', max_length=20, verbose_name='Повтор')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание события')),
                ('repeat_id', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.user')),
            ],
        ),
    ]
