# Generated by Django 4.2.2 on 2023-07-14 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_remove_movie_like_like'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ['liked_at']},
        ),
    ]
