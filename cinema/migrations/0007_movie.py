# Generated by Django 4.2.2 on 2023-06-08 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_delete_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cast', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='media/')),
                ('genre', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=200)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=100)),
                ('status', models.CharField(choices=[('Now Showing', 'Now Showing'), ('Coming Soon', 'Coming Soon')], max_length=100)),
                ('detail', models.TextField(blank=True)),
            ],
        ),
    ]
