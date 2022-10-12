from django.db import models
from datetime import datetime, timedelta


from api.models import Orders
from api.serializers import OrdersSerializer


# Create your models here.

ORDER_STAT = [
    ("0", "Ödeme Onayı Bekleniyor"),
    ("1", "Sipariş Hazırlanıyor"),
    ("2", "Sipariş Kargoda"),
    ("3", "Ödeme Hatası"),
    ("10", "Sipariş Tamamlandı"),
    ("20", "İptal talep edildi."),
    ("21", "İptal Onaylandı."),
    ("22", "İptal Reddedildi."),
]

ORDER_CANCEL_STAT = [
    ("0", "Kullanıcın kargoya vermesi bekleniyor."),
    ("1", "Kutunun satıcıya ulaşması bekleniyor."),
    ("2", "Satıcı onayı bekleniyor."),
    ("3", "Onaylandı. En kısa sürede ücret iadesi yapılacak."),
    ("4", "Reddedildi kutu tekrar müşteriye gönderiliyor."),
    ("5", "İade işlemi tamamlandı."),
]

ORDER_TYPE = [
    ("0", "Abonelik"),
    ("1", "Hediye"),
]


class OrderModel(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=True)
    price = models.FloatField(verbose_name="Tutar")
    subscription = models.ForeignKey(
        "subscription.SubscriptionModel", on_delete=models.CASCADE, blank=True, null=True)
    payment = models.BooleanField(verbose_name="Ödeme Durumu")
    date = models.DateTimeField(verbose_name="Tarih", auto_now_add=True)
    deliveryDate = models.DateTimeField(
        verbose_name="Teslim Tarihi", blank=True, null=True)
    order_type = models.CharField(
        verbose_name="Sipariş Türü", choices=ORDER_TYPE, max_length=8)
    status = models.CharField(
        verbose_name="Sipariş Durumu", max_length=30, choices=ORDER_STAT)
    cargo = models.CharField(verbose_name="Takip Kodu",
                             max_length=30, null=True, blank=True)
    fail_message = models.CharField(
        verbose_name="Hata Mesajı", max_length=50, null=True, blank=True)
    products = models.ManyToManyField("product.ProductModel")
    referenceCode = models.CharField(max_length=100)
    retry_count = models.IntegerField(default=0)
    retry_message = models.CharField(max_length=250, blank=True, null=True)
    birfatura_order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, blank=True, null=True)

    def order_can_be_canceled(self):
        if (self.status == "0" or self.status == "1" or self.status == "3") or self.can_be_canceled():
            return True
        return False

    def can_be_canceled(self):
        if self.deliveryDate:
            if datetime.now() - self.deliveryDate <= timedelta(days=14):
                return True
        return False

    def canceled(self):
        if self.status == "20" or self.status == "21":
            return True
        return False

    def save(self, *args, **kwargs):
        if self.status == "10" and not self.deliveryDate:
            self.deliveryDate = datetime.now()

        return super(OrderModel, self).save(*args, **kwargs)

    def create_bill(self, *args, **kwargs):
        if self.payment and not self.birfatura_order and not (self.status == "20" or self.status == "21"):
            from gift.models import GiftModel
            from api.models import PaymentMethods
            gm = GiftModel.objects.filter(order=self).first()
            validated_data = {
                "OrderId": self.pk,
                "OrderCode": str(self.pk),
                "TotalPaidTaxExcluding": self.price/1.18,
                "TotalPaidTaxIncluding": self.price,
                "ProductsTotalTaxExcluding": self.price/1.18,
                "ProductsTotalTaxIncluding": self.price,
                "Email": self.user.email,
                "Currency": "TRY",
                "OrderDetails": [],
                "PaymentTypeId": PaymentMethods.objects.get(id=1)
            }
            x = 0
            for p in self.products.all():
                x = x+p.price

            extra = (self.price - x) / len(self.products.all())

            for p in self.products.all():
                validated_data["OrderDetails"].append({
                    "ProductId": p.pk,
                    "ProductCode": p.code,
                    "ProductName": p.name,
                    "ProductQuantityType": "Adet",
                    "ProductQuantity": 1,
                    "VatRate": p.vat_rate,
                    "ProductUnitPriceTaxExcluding": p.unit_price,
                    "ProductUnitPriceTaxIncluding": p.price + extra
                })
            if gm:
                validated_data.setdefault("BillingName", gm.name)
                validated_data.setdefault("BillingAddress", gm.first_line)
                validated_data.setdefault("BillingTown", gm.district)
                validated_data.setdefault("BillingCity", gm.province)
                validated_data.setdefault("BillingMobilePhone", str(gm.phone))
            else:
                validated_data.setdefault(
                    "BillingName", self.user.get_full_name())
                validated_data.setdefault(
                    "BillingAddress", self.user.delivery_default_address.first_line)
                validated_data.setdefault(
                    "BillingTown", self.user.delivery_default_address.district)
                validated_data.setdefault(
                    "BillingCity", self.user.delivery_default_address.province)
                validated_data.setdefault(
                    "BillingMobilePhone", str(self.user.phone))

            validated_data["ShippingName"] = validated_data.get(
                "BillingName")
            validated_data["ShippingAddress"] = validated_data.get(
                "BillingAddress")
            validated_data["ShippingTown"] = validated_data.get(
                "BillingTown")
            validated_data["ShippingCity"] = validated_data.get(
                "BillingCity")

            validated_data = OrdersSerializer().create(
                validated_data=validated_data)

            self.birfatura_order = validated_data
            self.save()


class OrderCancelModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Durum",
                              max_length=20, choices=ORDER_CANCEL_STAT)
    date = models.DateTimeField(verbose_name="Tarih", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == "5":
            bfo = self.order.birfatura_order
            self.order.birfatura_order = None
            self.order.save()
            if bfo:
                bfo.delete()
        super(OrderCancelModel, self).save(
            *args, **kwargs)  # Call the real save() method
