# Generated by Django 4.1 on 2022-11-05 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_post_author_remove_post_likes_delete_comment_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Chat',
        ),
    ]
