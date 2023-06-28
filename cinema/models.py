from typing import Any
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
MOVIE_STATUS  =(('showing', 'showing'), ('comingsoon', 'comingsoon'))
SHIFT = (('M', 'M'),('D', 'D'),('N', 'N'))
STATUS = (('active', 'active'), ('inactive', 'inactive'))
SEAT_STATUS = (('available', 'available'), ('pending', 'pending'), ('reserved', 'reserved'))


class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    status = models.CharField(choices=STATUS, max_length=20)
    contact_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    