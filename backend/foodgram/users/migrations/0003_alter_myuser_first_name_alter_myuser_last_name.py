# Generated by Django 5.2.4 on 2025-07-08 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_myuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]
