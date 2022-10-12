from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.InfoSurvey)
class InfoSurvey(admin.ModelAdmin):
    fields = ('full_name', 'email', 'phone',)
    list_display = ('full_name', 'email', 'phone',)
    list_filter = ('full_name', 'email', 'phone',)
