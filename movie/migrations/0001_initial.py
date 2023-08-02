# Generated by Django 4.2.2 on 2023-07-24 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema', '0001_initial'),
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
                ('end_date', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(max_length=100)),
                ('active', models.CharField(blank=True, choices=[('active', 'active'), ('inactive', 'inactive')], max_length=100, null=True)),
                ('movie_status', models.CharField(blank=True, choices=[('showing', 'showing'), ('comingsoon', 'comingsoon')], max_length=100, null=True)),
                ('detail', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_date', models.DateField(unique=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('shift', models.CharField(choices=[('Morning', 'Morning'), ('Day', 'Day'), ('Night', 'Night')], max_length=10)),
                ('price', models.PositiveBigIntegerField()),
                ('cinema_hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema.cinemahall')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.PositiveBigIntegerField(default=0, null=True)),
                ('liked_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['liked_at'],
            },
        ),
    ]
