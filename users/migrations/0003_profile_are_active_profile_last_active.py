# Generated by Django 4.2 on 2023-05-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='are_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_active',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
