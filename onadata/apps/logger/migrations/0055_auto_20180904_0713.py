# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-04 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0054_instance_has_a_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submissionreview',
            name='deleted_at',
            field=models.DateTimeField(db_index=True, default=None, null=True),
        ),
    ]