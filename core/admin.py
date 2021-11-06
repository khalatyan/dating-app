from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import *

@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        ('Данные пользователя', {
            'fields': (
                'first_name', 'last_name', 'email', 'user_photo', 'user_photo_img', 'sex', 'longitude', 'latitude'
            )
        }),
        ('Редактирование полномочий', {
            'fields': (
                'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions', 'password'
            )
        })
    )
    list_display = [
        'id', 'email', 'first_name', 'last_name', 'user_photo_img'
    ]
    list_filter = (
        'is_staff', 'is_superuser', 'groups', 'date_joined'
    )
    search_fields = (
        'first_name', 'last_name', 'email'
    )
    readonly_fields = [
        'user_photo_img'
    ]
    ordering = ['email']


@admin.register(Estimation)
class EstimationAdmin(admin.ModelAdmin):
    list_display = [
        'who_rated', 'who_was_rated', 'estimation'
    ]

    search_fields = (
        'who_rated', 'who_was_rates'
    )

    list_filter = [
        'estimation'
    ]

