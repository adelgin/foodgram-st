from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True, default=None, 
                               upload_to='user_avatars')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Subscription(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False)
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE, 
                                  related_name='followers', null=False)
