# Generated by Django 4.2.2 on 2023-07-18 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=50)),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('address', models.CharField(max_length=50)),
                ('balance', models.PositiveBigIntegerField(default=0)),
            ],
        ),
    ]
