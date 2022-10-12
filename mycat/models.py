import sys

from django.db import models
# Create your models here.

GENDER = [
    ("0", "Dişi"),
    ("1", "Erkek"),
]

STATUS = [
    ("0", "Yavru"),
    ("1", "Yetişkin"),
    ("2", "Kısırlaştırılmış"),
]


class MyCatModel(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Kedi Adı", max_length=30)
    gender = models.CharField(verbose_name="Cinsiyet",
                              max_length=6, choices=GENDER)
    status = models.CharField(verbose_name="Durumu",
                              max_length=20, choices=STATUS)
    spec_case = models.TextField(
        verbose_name="Özel Durum", max_length=140, blank=True, null=True)
    picture = models.ImageField(verbose_name="Fotoğraf")
