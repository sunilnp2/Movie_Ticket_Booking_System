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
