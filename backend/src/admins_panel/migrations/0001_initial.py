# Generated by Django 5.1.4 on 2025-01-10 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Товар')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена товара')),
                ('quantity', models.IntegerField(verbose_name='Количество товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Операции')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена операции')),
            ],
            options={
                'verbose_name': 'Операция',
                'verbose_name_plural': 'Операции',
            },
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Работник')),
                ('work_place', models.CharField(max_length=50, verbose_name='Место работы')),
                ('admins_rights', models.BooleanField(default=False, verbose_name='Права админа')),
                ('salary', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='зарплата')),
            ],
            options={
                'verbose_name': 'Работник',
                'verbose_name_plural': 'Работники',
            },
        ),
        migrations.CreateModel(
            name='WorksDone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата выполнения работ')),
                ('quantity', models.IntegerField(verbose_name='Количество выполненных работ')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins_panel.operations')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admins_panel.worker')),
            ],
            options={
                'verbose_name': 'Выполненная работа',
                'verbose_name_plural': 'Выполненные работы',
            },
        ),
    ]
