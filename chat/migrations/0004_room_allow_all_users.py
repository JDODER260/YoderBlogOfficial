# Generated by Django 4.1 on 2023-05-22 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_room_allowed_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='allow_all_users',
            field=models.BooleanField(default=True),
        ),
    ]
