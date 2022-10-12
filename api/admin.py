from django.contrib import admin

from .models import OrderStatus, PaymentMethods, OrderDetailsModel, Orders

# Register your models here.


admin.site.register(OrderStatus)
admin.site.register(PaymentMethods)
admin.site.register(OrderDetailsModel)
admin.site.register(Orders)
