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

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('-date_joined', )

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'


class Subscription(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False)
    following = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                                  related_name='followers', null=False)
    created_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        verbose_name = 'Подписка'
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.user.username} подписан на {self.following.username}'
