# Generated by Django 5.1.4 on 2025-01-20 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins_panel', '0007_alter_operationlog_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='have_telegram',
            field=models.BooleanField(default=True, verbose_name='Есть телеграм'),
        ),
        migrations.AlterField(
            model_name='position',
            name='default_operation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admins_panel.operation'),
        ),
    ]
