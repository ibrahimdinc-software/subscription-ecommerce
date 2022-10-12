from django.core.management.base import BaseCommand

from subscription.models import SubscriptionModel
from order.models import OrderModel

from datetime import datetime, timedelta

from subscription import iyzic
from paymentapp.models import Conversation


import logging
db_logger = logging.getLogger('db')


class Command(BaseCommand):
    title = 'Abonelik Sipariş Kontrol'

    def handle(self, *args, **kwargs):
        subs = SubscriptionModel.objects.filter(status="1")
        for sub in subs:
            db_logger.info("Abonelik Sipariş Kontrol sub id: " + str(sub.id))
            orders = OrderModel.objects.filter(
                subscription=sub).order_by("-date")
            lod = orders[0].date
            pd = sub.pricing.time_to_pass()
            nod = lod+pd
            # sonraki sipariş tarhi(nod) ve şimdiki tarih arasındaki fark negatif mi

            if nod - datetime.now() <= timedelta(days=0):

                iyzisub = iyzic.Subscription(sub.referenceCode)
                iyziorder = iyzisub.orders[1]

                db_logger.info(
                    "Abonelik Sipariş Kontrol sub id: " + str(sub.id) + " tarih kontrol iyzisub: " + str(iyzisub))
                db_logger.info(
                    "Abonelik Sipariş Kontrol sub id: " + str(sub.id) + " tarih kontrol iyziorder: " + str(iyziorder))

                #! Tarihi gelmiş ve başarısız işlem varsa ödeme tekrarlama ekle
                if iyzisub.sub.get("data").get("subscriptionStatus") == "UNPAID":

                    db_logger.info(
                        "Abonelik Sipariş Kontrol sub id: " + str(sub.id) + " ödeme hatası var.")

                    order = OrderModel(
                        user=sub.user,
                        price=sub.pricing.pricing.get_discount_price(),
                        subscription=sub,
                        payment=False,
                        order_type="0",
                        status="3",
                        referenceCode=iyzisub.orders[0].get("referenceCode")
                    )
                    order.save()
                    order.products.set(
                        sub.pricing.pricing.secondaryProducts.all())
                    order.save()

                    db_logger.info(
                        "Abonelik Sipariş Kontrol sub id: " + str(sub.id) + " sipariş oluştu: " + str(order.id))

                elif self.date_converter(iyziorder.get("startPeriod"))-datetime.now() <= timedelta(days=0):
                    db_logger.info(
                        "Abonelik Sipariş Kontrol sub id: " + str(sub.id) + " tarih kontrol OK")
                    if iyziorder.get("orderStatus") == "SUCCESS":
                        db_logger.info(
                            "Abonelik Sipariş Kontrol sub id: " + str(sub.id) + " sipariş başarılı yeni sipariş oluştu: ")
                        order = OrderModel(
                            user=sub.user,
                            price=sub.pricing.pricing.get_discount_price(),
                            subscription=sub,
                            payment=False,
                            order_type="0",
                            status="0",
                            referenceCode=iyziorder.get("referenceCode")
                        )
                        order.save()
                        order.products.set(
                            sub.pricing.pricing.secondaryProducts.all())
                        order.save()

                        db_logger.info(
                            "Abonelik Sipariş Kontrol sub id: " + str(sub.id) + " sipariş başarılı yeni sipariş oluştu: " + str(order.id))

                        iyzisub.create_conversation(order)

    def date_converter(self, timestamp):
        return datetime.fromtimestamp(timestamp / 1000)
