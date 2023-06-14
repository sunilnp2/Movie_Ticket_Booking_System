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

class Movie(models.Model):
    name = models.CharField(max_length=200)
    cast = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/')
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=200)
    release_date = models.DateField(blank=True,null=True)
    slug = models.SlugField(max_length=100)
    active = models.CharField(choices=STATUS, max_length=100, blank=True, null=True)
    status = models.CharField(choices=MOVIE_STATUS, max_length=100)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Date(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class Showtime(models.Model):
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift = models.CharField(choices=SHIFT, max_length=10)
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return self.shift
    
    

# class Seat(models.Model):
#     date = models.ManyToManyField(Date, null=True, blank=True)
#     showtime = models.ManyToManyField(Showtime, null=True, blank=True)
#     seat_number = models.PositiveIntegerField()
#     name = models.CharField(max_length=10)
#     morning = models.BooleanField(default=True)
#     day = models.BooleanField(default=True)
#     night = models.BooleanField(default=True)

#     def __str__(self):
#         return str(self.seat_number)
    
#     def show_time(self):
#         return ",".join([str(p) for p in self.showtime.all()])
    
#     def show_date(self):
#         return ",".join([str(p) for p in self.date.all()])

class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    name = models.CharField(max_length=10)
    status = models.CharField(choices=SEAT_STATUS, max_length=100,blank=True, null=True)

    def __str__(self):
        return str(self.seat_number)


class SeatAvailability(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, blank=True, null=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    status = models.CharField(SEAT_STATUS, max_length=20, null=True, blank=True)
    morning = models.BooleanField(default=True)
    day = models.BooleanField(default=True)
    night = models.BooleanField(default=True)

    def __str__(self):
        return f"Seat {self.seat.seat_number} Availability"
    


# class Booking_History(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     date = models.DateField(auto_now_add=True)
#     showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
#     seat = models.ForeignKey(Seat, on_delete=models.CASCADE)







# Custom user registration part ---------------------------------------------------------------------------------------------

class MyUserManager(BaseUserManager):
    def create_user(self, email,first_name, last_name,phone,password=None, password2 = None):
        """
         Creates and saves a user with the given email, name, phone ,password
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        if not phone:
            raise ValueError("User must have phone")

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,first_name, last_name,phone, password=None, password2 = None):
        """
        Creates and saves a superuser with the given email, name, phone ,password
        """
        user = self.create_user(
            email,
            first_name = first_name, 
            last_name=last_name,
            phone = phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

    # create custom user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name="Username",
        max_length=255,
        unique=True,
        null=True,
    )

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=50)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

    
# class Booking(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
#     seat = models.ManyToManyField(Seat)
#     date = models.DateField(auto_now_add=True)
#     payment = models.CharField()

#     def __str__(self):
#         return self.user




