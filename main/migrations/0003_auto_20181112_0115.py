# Generated by Django 2.1.3 on 2018-11-12 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20181111_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userworkspace',
            name='privilege',
            field=models.BooleanField(verbose_name='is admin'),
        ),
    ]
