# Generated by Django 2.1.3 on 2018-11-21 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181112_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='invited',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]