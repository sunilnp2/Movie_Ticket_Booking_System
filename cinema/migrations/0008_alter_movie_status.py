# Generated by Django 4.2.2 on 2023-06-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='status',
            field=models.CharField(choices=[('showing', 'showing'), ('comingsoon', 'comingsoon')], max_length=100),
        ),
    ]
