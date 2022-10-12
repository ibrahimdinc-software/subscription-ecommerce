from django.contrib import admin
from django.http import HttpResponseRedirect
from rangefilter.filter import DateTimeRangeFilter
from . import models

# Register your models here.


class InlineOrderCancelModel(admin.TabularInline):
    model = models.OrderCancelModel
    extra = 0
    can_delete = False


@admin.register(models.OrderModel)
class AdminOrderModel(admin.ModelAdmin):
    change_form_template = "admin/order_billing.html"
    fields = (('user', 'price',),
              ('subscription', 'status', 'payment', 'order_type',), ('cargo', 'deliveryDate',), 'products', ('referenceCode', 'retry_count', 'retry_message',), 'birfatura_order')

    list_display = ('id', 'user', 'payment', 'order_type',
                    'status', 'date',)
    list_filter = (('date', DateTimeRangeFilter),
                   'payment', 'status', ('deliveryDate', DateTimeRangeFilter), )

    inlines = [InlineOrderCancelModel]

    def response_change(self, request, obj):
        if "_create_bill" in request.POST:
            obj.create_bill()
            self.message_user(request, "Bu sipariş için fatura oluşturuldu.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(models.OrderCancelModel)
class AdminOrderCancelModel(admin.ModelAdmin):
    fields = ('order', 'status', 'date')
    list_display = ('order', 'status', 'date')
    list_filter = ('order', 'status', 'date')
    readonly_fields = ('date',)


class InlineOrderModel(admin.TabularInline):
    model = models.OrderModel
    extra = 0
    can_delete = False
