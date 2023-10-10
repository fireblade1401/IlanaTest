import random

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import date


class UserProfileManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с указанным номером телефона и паролем.
        """
        if not phone_number:
            raise ValueError('Необходим номер телефона')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Создает и возвращает суперпользователя с указанным номером телефона и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

    def get_by_natural_key(self, phone_number):
        return self.get(phone_number=phone_number)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    USERNAME_FIELD = 'phone_number'
    objects = UserProfileManager()

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return self.username


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed')
    )
    user = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    order_number = models.PositiveIntegerField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    attachments = models.ManyToManyField('Attachment', blank=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super(Order, self).save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        number = random.randint(100000, 999999)
        while Order.objects.filter(order_number=number).exists():
            number = random.randint(100000, 999999)
        return number


class Attachment(models.Model):
    file = models.FileField(upload_to='order_attachments/')
