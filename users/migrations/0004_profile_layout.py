# Generated by Django 4.2 on 2023-05-04 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_are_active_profile_last_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='layout',
            field=models.BooleanField(default=False),
        ),
    ]
