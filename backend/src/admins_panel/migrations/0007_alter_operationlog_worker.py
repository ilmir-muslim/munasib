# Generated by Django 5.1.4 on 2025-01-19 00:16

import admins_panel.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins_panel', '0006_alter_goods_price_alter_operation_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationlog',
            name='worker',
            field=models.ForeignKey(default=admins_panel.models.Worker.get_deleted_worker, on_delete=django.db.models.deletion.SET_DEFAULT, to='admins_panel.worker'),
        ),
    ]
