# Generated by Django 4.2.2 on 2023-07-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_seat_seat_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='screen_visibility',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
