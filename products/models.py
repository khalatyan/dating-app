from django.db import models
from django.utils.html import format_html

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Меню сайта
    """

    parent = TreeForeignKey(
        'self',
        verbose_name='Родитель',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    href = models.CharField(
        verbose_name="Ссылка",
        max_length=4000
    )

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    class MPTTMeta:
        order_insertion_by = ['title']


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name=u'Категория',
        on_delete=models.CASCADE,
    )

    cost = models.FloatField(
        verbose_name='Цена',
        default=0,
    )

    title = models.CharField(
        verbose_name='Название',
        max_length=255
    )

    photo = models.ImageField(
        verbose_name=u'Фото',
        blank=True,
        null=True,
        upload_to='product-photo/'
    )

    def photo_img(self):
        image = '-'
        if self.photo:
            image = format_html('<img src="{0}" height="150"/>', self.photo.url)
        return image

    photo_img.allow_tags = True
    photo_img.short_description = u'Фото'

    def __str__(self):
        return '%s' % self.id

    class Meta:
        verbose_name = u'продукт'
        verbose_name_plural = u'Продукты'
