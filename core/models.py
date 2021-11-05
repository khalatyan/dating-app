from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

SEX = [
    (0, "Не указан"),
    (1, "Мужской"),
    (2, "Женский"),
]

class UserManager(BaseUserManager):
    '''
    Менеджер пользователей, который вместо имени пользователя в качестве
    уникального идентификатора использует номер телефона
    '''

    def create_user(self, email, password=None, **extra_fields):
        '''
        Создаёт и сохраняет пользователя с указанным номером телефона и паролем
        '''
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''
        Создаёт и сохраняет суперпользователя с указанным номером телефона и паролем
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    first_name = models.CharField(
        u'Имя',
        max_length=255,
        blank=True
    )

    last_name = models.CharField(
        u'Фамилия',
        max_length=255,
        blank=True
    )

    email = models.EmailField(
        max_length=254,
        unique=True
    )

    user_photo = models.ImageField(
        verbose_name=u'Фото пользователя',
        blank=True,
        null=True
    )

    sex = models.IntegerField(
        choices=SEX,
        verbose_name="Пол",
        default=0
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def user_photo_img(self):
        image = '-'
        if self.user_photo:
            image = format_html('<img src="{0}" height="150"/>', self.user_photo.url)
        return image
    user_photo_img.allow_tags = True
    user_photo_img.short_description = u'Фото пользователя'

    def __str__(self):
        return self.email