from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.CategoryModel)
class AdminCategoryModel(admin.ModelAdmin):
    fields = ('name', 'slug')
    list_display = ('name', 'slug')
    list_filter = ('name',)


def Update(modeladmin, request, queryset):
    queryset.update()


Update.short_description = "Güncelle"


@admin.register(models.ProductModel)
class AdminProductModel(admin.ModelAdmin):
    fields = ('name', 'code', 'category', 'unit_price',
              'vat_rate', 'price', 'picture')
    list_display = ('name', 'code', 'category', 'is_picture', 'price',)
    list_filter = ('name', 'category', 'price',)
    actions = [Update]
