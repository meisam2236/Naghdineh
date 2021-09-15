from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']
    if not extension.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension!')

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='files/user_avatars', null=True, blank=True, validators=[validate_file_extension])
    stock = models.IntegerField(default=0, blank=False)
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Transaction(models.Model):
    title = models.CharField(max_length=128, null=False, blank=False)
    price = models.IntegerField(default=0, blank=False)
    date_time = models.DateTimeField(default=datetime.now, blank=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    wallet_name = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField(max_length=128 ,null=False, blank=False)
    def __str__(self):
        return self.title

class Wallet(models.Model):
    title = models.CharField(max_length=128 ,null=False, blank=False)
    stock = models.IntegerField(default=0, blank=False)
    def __str__(self):
        return self.title