# Generated by Django 5.2.4 on 2025-07-08 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(default=None, null=True, upload_to='user_avatars'),
        ),
    ]
