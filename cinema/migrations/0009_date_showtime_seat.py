# Generated by Django 4.2.2 on 2023-06-08 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0008_alter_movie_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('shift', models.CharField(choices=[('M', 'M'), ('D', 'D'), ('N', 'N')], max_length=10)),
                ('price', models.PositiveBigIntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.date')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=10)),
                ('morning', models.BooleanField(default=True)),
                ('day', models.BooleanField(default=True)),
                ('night', models.BooleanField(default=True)),
                ('showtime', models.ManyToManyField(to='cinema.showtime')),
            ],
        ),
    ]
