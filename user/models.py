from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager, AbstractUser


from phonenumber_field.modelfields import PhoneNumberField

from datetime import datetime

from subscription import iyzic
# Create your models here.


COUNTRIES = [
    ('TR', 'Türkiye'),
]


class DeliveryAddress(models.Model):
    province = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    first_line = models.CharField(max_length=200, verbose_name="İlk Satır")

    def __str__(self):
        email = User.objects.filter(delivery_default_address=self).first()
        if email:
            email = email.email
            return email + " Adresi"
        return str(self.id) + " Adres"


class UserNotification(models.Model):
    is_read = models.BooleanField(default=False, verbose_name="Okundu Mu?")
    notification = models.ForeignKey(
        "notifications.Notification", verbose_name="Bildirim", on_delete=models.CASCADE)
    user = models.ForeignKey(
        "user.User", verbose_name="Kullanıcı", on_delete=models.CASCADE)
    time = models.DateTimeField("Tarih")

    def get_time(self):
        time = datetime.now()
        if self.time.month == time.month:

            if self.time.day == time.day:

                if self.time.hour == time.hour:
                    if time.minute - self.time.minute == 0:
                        return "Şimdi"
                    return str(time.minute - self.time.minute) + " dakika önce"

                return str(time.hour - self.time.hour) + " saat önce"

            return str(time.day - self.time.day) + " gün önce"

        return self.time


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=50, null=False, blank=True)
    last_name = models.CharField(max_length=50, null=False, blank=True)
    phone = PhoneNumberField()
    sub = models.ForeignKey(
        "subscription.SubscriptionModel", on_delete=models.CASCADE, null=True, blank=True, related_name="Subscription")
    is_tester = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ,
    )
    is_registered = models.BooleanField(
        'register status',
        default=True,
    )
    delivery_default_address = models.ForeignKey(
        to=DeliveryAddress, on_delete=models.CASCADE, related_name="userdefaddr", blank=True, null=True)

    referenceCode = models.CharField(
        verbose_name="iyzico referans", max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.phone and self.delivery_default_address and not self.referenceCode:
            ref = self.create_ref()
            if ref.get("status") == "success":
                self.referenceCode = ref.get("data").get("referenceCode")
            else:
                from notifications.notification import Notification
                Notification().add_notif_user(code="user_refcode", user=self)
                self.is_tester = False
        super(User, self).save(*args, **kwargs)  # Call the real save() method

    def create_ref(self):
        return iyzic.Customer().create(self)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    def is_subscribed(self):
        if self.sub:
            return True
        return False
