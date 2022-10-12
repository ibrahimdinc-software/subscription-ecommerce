from django.db import models
from datetime import datetime

from user.models import User, UserNotification

# Create your models here.


class Notification(models.Model):
    name = models.CharField(max_length=50, verbose_name="Bildirim Başlığı")
    content = models.CharField(max_length=200, verbose_name="Bildirim İçeriği")
    subject = models.ForeignKey(
        "Notification_Subject", on_delete=models.CASCADE, verbose_name="Konu")
    code = models.CharField(max_length=100, verbose_name="Bildirim Kodu")
    time = models.DateTimeField("Tarih")

    def __str__(self):
        return "Bildirim: " + self.name


class Notification_Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name="Konu")

    def __str__(self):
        return self.name
