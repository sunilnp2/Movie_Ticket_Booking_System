# Generated by Django 4.2.2 on 2023-07-29 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='seat_score',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]