from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

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
    