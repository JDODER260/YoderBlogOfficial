# Generated by Django 4.2 on 2023-05-04 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='background_img',
            field=models.ImageField(default='background.png', upload_to='post_backgrounds'),
        ),
    ]
