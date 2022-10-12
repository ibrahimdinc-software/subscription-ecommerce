from django.db import models

# Create your models here.
import logging
db_logger = logging.getLogger('db')


class OrderStatus(models.Model):
    value = models.CharField(max_length=20, verbose_name="Durum")


class PaymentMethods(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    value = models.CharField(max_length=20, verbose_name="Metod")


class OrderDetailsModel(models.Model):
    ProductId = models.IntegerField()
    ProductCode = models.CharField(max_length=30)
    ProductName = models.CharField(max_length=50)
    ProductQuantityType = models.CharField(max_length=30)
    ProductQuantity = models.IntegerField()
    VatRate = models.IntegerField()
    ProductUnitPriceTaxExcluding = models.FloatField()
    ProductUnitPriceTaxIncluding = models.FloatField()

    def __str__(self):
        return str(self.id) + ' ' + self.ProductName


class Orders(models.Model):
    OrderId = models.IntegerField(primary_key=True, unique=True)
    OrderCode = models.CharField(max_length=10)
    OrderDate = models.DateTimeField(auto_now_add=True)
    BillingName = models.CharField(max_length=100)
    BillingAddress = models.CharField(max_length=300)
    BillingTown = models.CharField(max_length=30)
    BillingCity = models.CharField(max_length=30)
    BillingMobilePhone = models.CharField(max_length=30)
    ShippingName = models.CharField(max_length=30)
    ShippingAddress = models.CharField(max_length=300)
    ShippingTown = models.CharField(max_length=30)
    ShippingCity = models.CharField(max_length=30)
    PaymentTypeId = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    Currency = models.CharField(max_length=30)
    Email = models.CharField(max_length=100)
    TotalPaidTaxExcluding = models.FloatField(
        verbose_name="Kdv hariç ödenecek toplam tutar")
    TotalPaidTaxIncluding = models.FloatField(
        verbose_name="Kdv dahil ödenecek toplam tutar")
    ProductsTotalTaxExcluding = models.FloatField(
        verbose_name="Kdv hariç ürünlerin toplam tutarı")
    ProductsTotalTaxIncluding = models.FloatField(
        verbose_name="Kdv dahil ürünlerin toplam tutarı")
    OrderDetails = models.ManyToManyField(
        "api.OrderDetailsModel", blank=True)

    def delete(self, *args, **kwargs):
        ods = self.OrderDetails.all()
        db_logger.info(str(self.OrderId) + ' fatura' + ' silindi')
        for od in ods:
            db_logger.info(str(od) + ' silindi')
            print(od)
            od.delete()
        # Call the real delete() method
        super(Orders, self).delete(*args, **kwargs)
