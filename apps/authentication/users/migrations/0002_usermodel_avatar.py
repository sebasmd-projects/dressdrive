# Generated by Django 4.1.5 on 2023-01-31 07:37

import apps.authentication.users.signals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=apps.authentication.users.signals.avatar_directory_path, verbose_name='profile picture'),
        ),
    ]