from math import sin, cos, sqrt, atan2, radians

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

ESTIMATION = [
    (-1, "Дизлайк"),
    (1, "Лайк"),
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
    username = None

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
        null=True,
        upload_to='user-photo/'
    )

    sex = models.IntegerField(
        choices=SEX,
        verbose_name="Пол",
        default=0
    )

    longitude = models.FloatField(
        verbose_name='Долгота',
        default=0,
    )

    latitude = models.FloatField(
        verbose_name='Широта',
        default=0,
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

    def get_user_distance(self, user):
        EARTH_RADIUS = 6373.0

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(user.latitude)
        lon2 = radians(user.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = EARTH_RADIUS * c
        return distance

    def get_user_photo_path(self):
        if self.user_photo:
            return "http://127.0.0.1:8000" + str(self.user_photo.url)
        else:
            return None

    def __str__(self):
        return self.email


class Estimation(models.Model):
    who_rated = models.ForeignKey(
        User,
        verbose_name=u'Кто оценил',
        on_delete=models.CASCADE,
        related_name='who_rated_user'
    )

    who_was_rated = models.ForeignKey(
        User,
        verbose_name=u'Кого оценили',
        on_delete=models.CASCADE,
        related_name='who_was_rated_user'
    )

    estimation = models.IntegerField(
        choices=ESTIMATION,
        verbose_name="Оценка",
        default=-1
    )

    def __str__(self):
        return '%s' % self.id

    class Meta:
        unique_together = ('who_rated', 'who_was_rated',)
        verbose_name = u'оценка'
        verbose_name_plural = u'Оценки'
