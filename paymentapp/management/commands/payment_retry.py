from django.core.management.base import BaseCommand

from order.models import OrderModel

from subscription import iyzic


import logging
db_logger = logging.getLogger('db')


class Command(BaseCommand):
    title = 'Ödeme Tekrar Deneme'

    def handle(self, *args, **kwargs):
        os = OrderModel.objects.filter(status="3")

        for o in os:
            if o.subscription and o.retry_count < 10:
                db_logger.info("Ödeme Tekrar Deneme sipariş no: " + str(o.id))
                iyzisub = iyzic.Subscription(o.subscription.referenceCode)
                result = iyzisub.retry(o)
                print(result)

                db_logger.info("Ödeme Tekrar Deneme result: " + str(result))

                if result.get("status") != "success":
                    o.retry_count += 1
                    o.retry_message = result.get("errorMessage")
                    o.save()
