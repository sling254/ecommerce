from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager

# Create your models here.
Gender = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('intersex', 'Intersex'),
)
USER_ROLES = (
    (1, 'customer'),
    (2, 'supplier'),
    (3, 'courrier'),
)

class User(AbstractBaseUser, PermissionsMixin):
    role = models.PositiveSmallIntegerField('Select User Type',choices=USER_ROLES)
    username = models.CharField(max_length=20, null=True, blank=True,unique=True,db_index=True)
    phone = models.CharField(max_length=12, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    county = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    is_actie = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    #instanciate the manager class
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'username', 'phone']

    def __str__(self):
        return self.email


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE,blank= True, null=True)
    county = models.CharField(max_length=20,blank= True, null=True)
    gender = models.CharField(max_length=20,choices=Gender, default=Gender)

    def __str__(self):
        return self.gender


class Courrier(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE,blank= True, null=True)
    company = models.CharField(max_length=20, blank= True, null=True)
  
    def __str__(self):
        return self.company
    
class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE,blank= True, null=True)
    lever = models.CharField(max_length=20,blank=True, null=True)

    
    def __str__(self):
        return self.lever



