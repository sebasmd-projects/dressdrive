# Generated by Django 4.1.5 on 2023-01-31 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_usermodel_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='privacy',
            field=models.BooleanField(default=False, verbose_name='Terms and Conditions'),
        ),
    ]
