from django.contrib import admin

from . import models
# Register your models here.


@admin.register(models.MyCatModel)
class AdminMyCatModel(admin.ModelAdmin):
    fields = (('name', 'gender',),
              ('status',), 'spec_case', 'picture',)
    list_display = ('user', 'name', 'gender', 'status',)
    list_filter = ('user', 'name', 'gender', 'status',)
