from django.db import models

from order.models import OrderModel

from notifications.notification import Notification

from . import iyzic

import logging
db_logger = logging.getLogger('db')

# Create your models here.
SUB_STAT = [
    ("0", "Pasif"),
    ("1", "Aktif"),
]

CANCEL_STATUS = [
    ("0", "Onay Bekliyor"),
    ("1", "Onaylandı"),
    ("2", "Reddedildi"),
]

PRICING_TYPE = [
    ("0", "Abonelik"),
    ("1", "Hediye"),
    ("2", "Özel"),
]

INTERVAL = [
    ("DAILY", "Günlük"),
    ("WEEKLY", "Haftalık"),
    ("MONTHLY", "Aylık"),
]


class PricingFeatureModel(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(verbose_name="Gösterme Sırası")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PricingPlanModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="İsim")
    interval = models.CharField(
        verbose_name="Aralık", choices=INTERVAL, max_length=30)
    frequency = models.IntegerField(verbose_name="Sıklık")
    pricing = models.ForeignKey(
        "subscription.PricingModel", verbose_name="Fiyatlandırma", on_delete=models.CASCADE)
    referenceCode = models.CharField(
        verbose_name="iyzico referans", max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.referenceCode:
            self.referenceCode = iyzic.Plan().create(self)
        if "özel" in self.name:
            self.name = "Özel"
        super(PricingPlanModel, self).save(
            *args, **kwargs)  # Call the real save() method

    def delete_reference(self, *args, **kwargs):
        self.referenceCode = '0'
        self.save()
        mes = iyzic.Plan().delete(self)
        return mes

    def time_to_pass(self):
        from dateutil.relativedelta import relativedelta
        if self.interval == "DAILY":
            return relativedelta(days=+1*self.frequency)
        elif self.interval == "WEEKLY":
            return relativedelta(weeks=1*self.frequency)
        elif self.interval == "MONTHLY":
            return relativedelta(months=+1*self.frequency)


class PricingModel(models.Model):
    name = models.CharField(max_length=155)
    code = models.CharField(max_length=55, unique=True, primary_key=True)
    features = models.ManyToManyField(
        PricingFeatureModel, blank=True)
    first_price = models.FloatField()
    discount = models.FloatField()
    picture = models.FileField(blank=True, null=True)
    pricing_type = models.CharField(
        verbose_name="Paket Türü", choices=PRICING_TYPE, max_length=8)
    order = models.IntegerField(verbose_name="Gösterme Sırası")
    products = models.ManyToManyField(
        "product.ProductModel", blank=True)
    secondaryProducts = models.ManyToManyField(
        "product.ProductModel", related_name="sproduct", blank=True)
    referenceCode = models.CharField(
        verbose_name="iyzico referans", max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.referenceCode and self.pricing_type != "1":
            self.referenceCode = iyzic.Product().create(self)
            print(self.referenceCode)
        print("self.referenceCode")
        # Call the real save() method
        super(PricingModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def selected_plan(self):
        if self.referenceCode:
            ppm = PricingPlanModel.objects.filter(pricing=self)
            return ppm[0].referenceCode
        return None

    def get_discount_price(self):
        return self.get_full_price() - self.discount

    def get_full_price(self):
        return self.first_price

    def get_features(self):
        return "\n".join([f.name for f in self.features.all().order_by("order")])


class SubscriptionManager(models.Manager):
    def subs(self):
        return super().get_queryset().order_by('-date')


class SubscriptionModel(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, blank=True, null=True)
    pricing = models.ForeignKey(
        PricingPlanModel, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")
    price = models.FloatField(verbose_name="Fiyat")
    status = models.CharField(
        verbose_name="Abonelik Durumu", max_length=30, choices=SUB_STAT)

    discount = models.FloatField(verbose_name="Abonelik İndirimi")
    referenceCode = models.CharField(max_length=100)

    objects = models.Manager()
    SubscriptionManager = SubscriptionManager()

    def save(self, *args, **kwargs):
        super(SubscriptionModel, self).save(*args, **kwargs)
        self.user.sub = self
        self.user.save()

    def get_discount_price(self):
        return self.price - self.discount

    def __str__(self):
        return self.user.email + " Aboneliği"


class CancelSubscription(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    subscription = models.ForeignKey(
        SubscriptionModel, on_delete=models.CASCADE)
    is_approved = models.CharField(
        verbose_name="Durum", choices=CANCEL_STATUS, default="0", max_length=20)
    description = models.CharField(
        verbose_name="Açıklama", blank=True, null=True, max_length=140)
    date = models.DateTimeField(verbose_name="Tarih", auto_now_add=True)
    order_cancel = models.BooleanField(
        verbose_name="Sipariş İptal Edildi Mi?", default=False)

    def save(self, *args, **kwargs):
        if self.is_approved == "1":

            db_logger.info("Abonelik iptal onaylandı: " + str(self.user.email))

            s = iyzic.Subscription().cancel(self.subscription.referenceCode)
            if s.get("status") != "success":
                db_logger.info("Abonelik iptal başarısız.")
                return s

            self.subscription.status = "0"
            self.subscription.save()
            notif = Notification()
            notif.add_notif_user("cancel_sub", self.user)

            self.delete()
        elif self.is_approved == "2":
            db_logger.info("Abonelik iptal reddedildi: " +
                           str(self.user.email))

            notif = Notification()
            notif.add_notif_user(None, self.user, message=self.description)
            self.delete()
        else:
            super(CancelSubscription, self).save(
                *args, **kwargs)  # Call the real save() method
