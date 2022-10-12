from django.contrib import admin

# Register your models here.

from . import models


@admin.register(models.Notification)
class AdminNotification(admin.ModelAdmin):
    fields = (('name', 'subject'), 'code', 'content', 'time')
    list_display = ('name', 'code', 'subject',  'content', 'time')
    list_filter = ('name', 'subject')


@admin.register(models.Notification_Subject)
class AdminNotification_Subject(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
