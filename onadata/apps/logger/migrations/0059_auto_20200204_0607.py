# Generated by Django 2.2.9 on 2020-02-04 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0058_auto_20191211_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xform',
            name='uuid',
            field=models.CharField(db_index=True, default='', max_length=36),
        ),
    ]
