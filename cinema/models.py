from django.db import models
from django.db import models
# Create your models here.

STATUS = (('active', 'active'), ('inactive', 'inactive'))


class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    hall_status = models.CharField(choices=STATUS, max_length=20, null=True, blank=True)
    contact_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    