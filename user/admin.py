from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import User, DeliveryAddress, UserNotification

# Register your models here.

admin.site.site_header = "MeowMeow.com.tr Yönetim Paneli"


class InlineUserNotifications(admin.TabularInline):
    model = UserNotification
    extra = 0
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_form_template = "admin/user_refcode.html"
    fields = ('email', 'first_name', 'last_name', 'phone', 'sub', 'delivery_default_address',
              ('is_tester', 'is_staff', 'is_active', 'is_registered',), 'referenceCode')
    list_display = ('email', 'first_name', 'last_name',
                    'is_subscribed', 'phone', 'referenceCode')
    list_filter = ('email', 'first_name', 'phone')

    inlines = [InlineUserNotifications]

    def response_change(self, request, obj):
        if "_create_refcode" in request.POST:
            ref = obj.create_ref()
            if ref.get("status") == "success":
                obj.referenceCode = ref.get("data").get("referenceCode")
                obj.is_tester = True
                obj.save()
                self.message_user(request, "İşlem başarılı.")
            else:
                self.message_user(request, ref.get("errorMessage"))
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    fields = ('user', 'notification', 'is_read', 'time',)
    list_display = ('user', 'notification', 'is_read', 'time',)
    list_filter = ('user', 'notification', 'is_read', 'time',)
