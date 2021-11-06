from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from products.models import *


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, admin.ModelAdmin):
    mptt_indent_field = "title"
    list_display = [
        'tree_actions', 'indented_title', 'href'
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'cost', 'photo_img'
    ]
    readonly_fields = [
        'photo_img'
    ]
