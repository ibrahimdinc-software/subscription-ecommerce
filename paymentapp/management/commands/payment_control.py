from django.core.management.base import BaseCommand

from order.models import OrderModel, OrderCancelModel

from paymentapp.payment import Pay

from paymentapp.models import Conversation


import logging
db_logger = logging.getLogger('db')


class Command(BaseCommand):
    title = 'Ödeme Kontrol'

    def handle(self, *args, **kwargs):
        os = OrderModel.objects.filter(payment=False)
        cs = Conversation.objects.all()
        ocm = OrderCancelModel.objects.all()
        p = Pay()

        for o in os:
            db_logger.info("Ödeme Kontrol: " + str(o.id))
            c = cs.filter(order=o).first()
            if c:
                oc = ocm.filter(order=o).first()
                pcres = p.payment_control(int(c.paymentId))
                print(pcres)
                db_logger.info("Ödeme Kontrol: " + str(o.id) +
                               ' sonuç: ' + str(pcres))
                if not oc and pcres.get('status') == 'success':
                    if pcres.get('paymentStatus') == 'SUCCESS':
                        o.payment = True
                        o.status = '1'
                        o.save()
