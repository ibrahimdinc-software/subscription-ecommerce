from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class GiftModel(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, blank=True, null=True)
    catname = models.CharField(
        max_length=50, verbose_name="Kedinin Adı", null=True, blank=True)
    spec_case = models.CharField(
        verbose_name="Özel Durum", blank=True, null=True, max_length=200)
    want_bag = models.CharField(
        verbose_name="Çanta istiyor mu?", blank=True, null=True, max_length=200)
    spec_note = models.CharField(
        verbose_name="Özel Not", blank=True, null=True, max_length=200)

    name = models.CharField(verbose_name="Ad Soyad", max_length=50)
    phone = PhoneNumberField()
    province = models.CharField(verbose_name="İl", max_length=20)
    district = models.CharField(verbose_name="İlçe", max_length=20)
    first_line = models.CharField(verbose_name="Açık Adres", max_length=200)

    order = models.ForeignKey(
        "order.OrderModel", blank=True, null=True, on_delete=models.CASCADE)

    date = models.DateTimeField(verbose_name="Tarih", auto_now_add=True)
