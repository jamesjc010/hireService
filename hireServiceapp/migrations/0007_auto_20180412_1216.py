# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-12 12:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hireServiceapp', '0006_orderdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hireServiceapp.Driver'),
        ),
    ]
