from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class InfoSurvey(models.Model):
    full_name = models.CharField(max_length=50, verbose_name="Ad Soyad")
    email = models.EmailField(
        verbose_name="E-Posta Adresi", max_length=50, unique=True)
    phone = PhoneNumberField(null=True, blank=True)