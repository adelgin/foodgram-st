from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Subscription

UserModel = get_user_model()


@admin.register(UserModel)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Дополнительно',
                                        {'fields': ('avatar', )}), )
    search_fields = ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'following__username', 'user__email',
                     'following__email')
