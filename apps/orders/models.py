import random

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import date


class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField()
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    USERNAME_FIELD = 'phone_number'

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
