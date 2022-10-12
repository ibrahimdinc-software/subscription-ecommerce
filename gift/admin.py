from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.GiftModel)
class AdminGiftModel(admin.ModelAdmin):
    fields = (('user', 'catname', 'spec_case', 'want_bag', 'spec_note',),
              ('name', 'phone', 'province', 'district', 'first_line',), 'order',)
    list_display = ('user', 'date',)
    list_filter = ('user', 'date',)
