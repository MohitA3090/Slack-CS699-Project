# Generated by Django 2.1.3 on 2018-11-11 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_on', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Channel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserWorkSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege', models.BooleanField(choices=[('A', 'Admin'), ('N', 'Not Admin')], verbose_name='is admin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.User')),
            ],
        ),
        migrations.CreateModel(
            name='WorkSpace',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.User')),
            ],
        ),
        migrations.AddField(
            model_name='userworkspace',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.WorkSpace'),
        ),
        migrations.AddField(
            model_name='channel',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.User'),
        ),
        migrations.AddField(
            model_name='channel',
            name='workspace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.WorkSpace'),
        ),
    ]
