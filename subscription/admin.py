from django.contrib import admin
from django.http import HttpResponseRedirect

from . import models
from order.admin import InlineOrderModel
# Register your models here.


@admin.register(models.PricingPlanModel)
class AdminPricingPlanModel(admin.ModelAdmin):
    change_form_template = "admin/pricingdelete.html"
    fields = ('name', 'interval', 'frequency', 'pricing', 'referenceCode')
    list_display = ('name', 'interval', 'frequency',
                    'pricing', 'referenceCode')
    list_filter = ('name', 'interval', 'frequency', 'pricing',)

    def response_change(self, request, obj):
        if "delete" in request.POST:
            subs = models.SubscriptionModel.objects.filter(pricing=obj)
            if subs:
                self.message_user(request, "Bu plan için abonelik bulunuyor.")
                return HttpResponseRedirect(".")
            else:
                mes = obj.delete_reference()
                self.message_user(request, mes)
                return HttpResponseRedirect(".")
        return super().response_change(request, obj)


@admin.register(models.PricingFeatureModel)
class AdminPricingFeatureModel(admin.ModelAdmin):
    fields = ('name', 'order',)
    list_display = ('name', 'order',)
    list_filter = ('name',)


@admin.register(models.PricingModel)
class AdminPricing(admin.ModelAdmin):
    fields = (('name', 'code',), 'features',
              ('first_price', 'discount'), 'pricing_type', 'picture', 'products', 'secondaryProducts', 'order', 'referenceCode')
    list_display = ('name', 'code',
                    'get_discount_price', 'pricing_type', 'order', 'referenceCode')
    list_filter = ('name', 'code',  'pricing_type',)

    def get_features(self, obj):
        return "\n".join([f.name for f in obj.features.all().order_by("order")])


class InlineCancelSubscription(admin.TabularInline):
    model = models.CancelSubscription
    extra = 0
    max_num = 1
    can_delete = False
    fields = ('is_approved', 'description',)


@admin.register(models.SubscriptionModel)
class AdminSubscriptionModel(admin.ModelAdmin):
    fields = ('user', 'pricing',
              ('price', 'discount', 'status',),  'date', 'referenceCode')
    readonly_fields = ('date',)
    list_display = ('user', 'pricing', 'status', 'date',)
    list_filter = ('pricing', 'status', 'date',)
    search_fields = ('user__email',)

    inlines = [InlineCancelSubscription,
               InlineOrderModel]


@admin.register(models.CancelSubscription)
class AdminCancelSubscription(admin.ModelAdmin):
    fields = ('user', 'subscription', 'is_approved', 'description',)
    list_display = ('user', 'is_approved', 'date',)
    list_filter = ('user', 'is_approved', 'date',)
