# Generated by Django 4.2.7 on 2023-12-04 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3, verbose_name='Категория')),
                ('description', models.CharField(max_length=60, verbose_name='Транспортное средстов')),
            ],
            options={
                'db_table': 'doc_app_driver_category',
            },
        ),
        migrations.CreateModel(
            name='DriverCategoryShedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_begin', models.DateField(default=None, null=True, verbose_name='Начало действия')),
                ('date_end', models.DateField(default=None, null=True, verbose_name='Окончание действия')),
                ('note', models.CharField(blank=True, max_length=5, null=True, verbose_name='Отметка о категории')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc_app.drivercategory', verbose_name='Категория')),
            ],
            options={
                'db_table': 'doc_app_driver_category_shedule',
            },
        ),
        migrations.CreateModel(
            name='ForeignPassport',
            fields=[
                ('series', models.CharField(max_length=10, null=True, verbose_name='Серия')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('date_registration', models.DateField(verbose_name='Дата выдачи')),
                ('id_inspection', models.IntegerField(blank=True, null=True, verbose_name='Код подразделения')),
                ('name_inspection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название подразделения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_app.user')),
                ('foreign_name', models.CharField(max_length=50, verbose_name='Имя латиницей')),
                ('foreign_surname', models.CharField(max_length=50, verbose_name='фамилия латиницей')),
                ('date_end_action', models.DateField(verbose_name='Дата окончания')),
            ],
            options={
                'db_table': 'doc_app_foreign_pass',
            },
        ),
        migrations.CreateModel(
            name='Inn',
            fields=[
                ('series', models.CharField(max_length=10, null=True, verbose_name='Серия')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('date_registration', models.DateField(verbose_name='Дата выдачи')),
                ('id_inspection', models.IntegerField(blank=True, null=True, verbose_name='Код подразделения')),
                ('name_inspection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название подразделения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_app.user')),
                ('inn', models.IntegerField(verbose_name='ИНН')),
            ],
            options={
                'db_table': 'doc_app_inn',
            },
        ),
        migrations.CreateModel(
            name='MilitaryTicket',
            fields=[
                ('series', models.CharField(max_length=10, null=True, verbose_name='Серия')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('date_registration', models.DateField(verbose_name='Дата выдачи')),
                ('id_inspection', models.IntegerField(blank=True, null=True, verbose_name='Код подразделения')),
                ('name_inspection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название подразделения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_app.user')),
                ('category', models.CharField(blank=True, choices=[('A', 'А - Годен'), ('B', 'Б - Годен с небольшими ограничениями'), ('C', 'В - Ограниченно годен'), ('D', 'Г - Временно не годен'), ('E', 'Д - Не годен')], max_length=40, null=True, verbose_name='Призывная категория')),
                ('speciality', models.CharField(max_length=50, verbose_name='Военная специальность')),
                ('description', models.TextField(verbose_name='Дополнительные сведения')),
            ],
            options={
                'db_table': 'doc_app_military_ticket',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('series', models.CharField(max_length=10, null=True, verbose_name='Серия')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('date_registration', models.DateField(verbose_name='Дата выдачи')),
                ('id_inspection', models.IntegerField(blank=True, null=True, verbose_name='Код подразделения')),
                ('name_inspection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название подразделения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_app.user')),
                ('adress_registration', models.CharField(blank=True, max_length=100, null=True, verbose_name='Адрес регистрации')),
                ('date_adress_reg', models.DateField(blank=True, null=True, verbose_name='Дата регистрации')),
                ('adress_reg_eq_place', models.BooleanField(default=False, verbose_name='Совпадает с адресом проживания')),
            ],
            options={
                'db_table': 'doc_app_passport',
            },
        ),
        migrations.CreateModel(
            name='Snils',
            fields=[
                ('series', models.CharField(max_length=10, null=True, verbose_name='Серия')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('date_registration', models.DateField(verbose_name='Дата выдачи')),
                ('id_inspection', models.IntegerField(blank=True, null=True, verbose_name='Код подразделения')),
                ('name_inspection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название подразделения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_app.user')),
            ],
            options={
                'db_table': 'doc_app_snils',
            },
        ),
        migrations.CreateModel(
            name='Spouce',
            fields=[
                ('surname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(blank=True, choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=7, null=True, verbose_name='Пол')),
                ('date_marriage', models.DateField(blank=True, null=True, verbose_name='Дата регистрации брака')),
                ('passport', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='doc_app.passport')),
            ],
            options={
                'db_table': 'doc_app_spouce',
            },
        ),
        migrations.CreateModel(
            name='DriverLicense',
            fields=[
                ('series', models.CharField(max_length=10, null=True, verbose_name='Серия')),
                ('number', models.IntegerField(verbose_name='Номер')),
                ('date_registration', models.DateField(verbose_name='Дата выдачи')),
                ('id_inspection', models.IntegerField(blank=True, null=True, verbose_name='Код подразделения')),
                ('name_inspection', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название подразделения')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user_app.user')),
                ('date_end_action', models.DateField(verbose_name='Окончание действия')),
                ('date_start_expirience', models.DateField(blank=True, null=True, verbose_name='Начало стажа')),
                ('special_marks', models.CharField(blank=True, max_length=40, null=True, verbose_name='Особые отметки')),
                ('categories', models.ManyToManyField(blank=True, through='doc_app.DriverCategoryShedule', to='doc_app.drivercategory', verbose_name='Разрешенные категории')),
            ],
            options={
                'db_table': 'doc_app_driver_license',
            },
        ),
        migrations.AddField(
            model_name='drivercategoryshedule',
            name='driver_license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doc_app.driverlicense', verbose_name='ВУ'),
        ),
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя')),
                ('patronymic', models.CharField(blank=True, max_length=50, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(blank=True, choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')], max_length=7, null=True, verbose_name='Пол')),
                ('passport', models.ManyToManyField(to='doc_app.passport')),
            ],
            options={
                'db_table': 'doc_app_children',
            },
        ),
    ]
