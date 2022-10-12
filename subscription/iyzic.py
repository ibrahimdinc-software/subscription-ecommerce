
from datetime import datetime
import json
from . import iyzi

from django.utils.crypto import get_random_string

from paymentapp.models import Conversation


import logging
db_logger = logging.getLogger('db')


def res(response):
    return json.loads(response.read().decode('utf-8'))


class Product():
    def create(self, product):
        r = iyzi.Product().create(request={
            'name': product.name
        }, foptions=iyzi.options)
        r = res(r)
        db_logger.info("Ürün oluşturma cevabı: " + str(r))
        if r.get("status") == "success":
            return r.get("data").get("referenceCode")
        else:
            random_str = get_random_string(length=10)
            product.name = product.name.split("-")[1] + "-" + random_str
            product.save()
            self.create(product)
        return None


class Plan():
    def create(self, plan):
        r = iyzi.Plan().create(request={
            'productReferenceCode': plan.pricing.referenceCode,
            'name': plan.pricing.name + ' ' + plan.name,
            'price': plan.pricing.get_discount_price(),
            'currencyCode': "TRY",
            'paymentInterval': plan.interval,
            'paymentIntervalCount': plan.frequency,
            'planPaymentType': "RECURRING"
        }, foptions=iyzi.options)

        r = res(r)

        db_logger.info("Plan oluşturma cevabı: " + str(r))

        if r.get("status") == "success":
            return r.get("data").get("referenceCode")

        return None

    def delete(self, plan):
        r = iyzi.Plan().delete(request={
            'pricingPlanReferenceCode': plan.referenceCode
        }, foptions=iyzi.options)
        r = res(r)

        db_logger.info("Plan silme cevabı: " + str(r))

        return r.get("status")


class Customer():
    def create(self, customer):
        r = iyzi.Customer().create(request={
            'name': customer.first_name,
            'surname': customer.last_name,
            'identityNumber': '11111111111',
            'email': customer.email,
            'gsmNumber': str(customer.phone),
            'billingAddress': {
                'contactName': customer.get_full_name(),
                'city': customer.delivery_default_address.province,
                'district': customer.delivery_default_address.district,
                'country': "Türkiye",
                'address': customer.delivery_default_address.first_line
            },
            'billingAddress': {
                'contactName': customer.get_full_name(),
                'city': customer.delivery_default_address.province,
                'district': customer.delivery_default_address.district,
                'country': "Türkiye",
                'address': customer.delivery_default_address.first_line
            }
        }, foptions=iyzi.options)

        r = res(r)

        db_logger.info("Müşteri oluşturma cevabı: " + str(r))

        return r


class Subscription():

    def __init__(self, referenceCode=None):
        if referenceCode:
            self.sub = self.detail(referenceCode)
            self.orders = self.sub.get("data").get("orders")
        super(Subscription, self).__init__()

    def detail(self, referenceCode):
        r = iyzi.Subscription().detail(request={
            "locale": "tr",
            "subscriptionReferenceCode": referenceCode
        }, foptions=iyzi.options)

        db_logger.info("Abonelik detay cevabı: " + str(r))

        return res(r)

    def cancel(self, referenceCode):
        r = iyzi.Subscription().cancel(request={
            "subscriptionReferenceCode": referenceCode
        }, foptions=iyzi.options)
        r = res(r)

        db_logger.info("Abonelik iptal cevabı: " + str(r))

        return r

    def retry(self, order):
        r = iyzi.Subscription().retry(request={
            "referenceCode": order.referenceCode
        }, foptions=iyzi.options)
        r = res(r)

        db_logger.info("Abonelik tekrar cevabı: " + str(r))

        if r.get("status") == "success":
            if self.sub.get("data").get("subscriptionStatus") == "ACTIVE":
                order.status = "1"
                order.retry_message = "Ödeme başarılı."
                order.save()
                #! sıralama değişiyor mu?
                self.create_conversation(order)
        return r

    def create_conversation(self, order):
        db_logger.info("Abonelik create_conversation: " + str(order))

        con = self.orders[1].get("paymentAttempts")
        if len(con) > 0:
            print(con)
            con = con[0]
            cons = Conversation.objects.filter(
                conversationId=con.get("conversationId")).first()
            print(datetime.fromtimestamp(con.get("createdDate") / 1000))
            if cons:
                return

            conversation = Conversation(
                order=order,
                conversationId=con.get("conversationId"),
                status=con.get("paymentStatus"),
                paymentId=str(con.get("paymentId")),
                is_pay=False
            )
            conversation.save()

    def cardUpdate(self, referenceCode):
        r = iyzi.Subscription().cardupdate(request={
            "locale": "tr",
            "subscriptionReferenceCode": referenceCode,
            "callbackUrl": "https://meowmeow.com.tr/subscription/newcardsuccess"
        }, foptions=iyzi.options)

        r = res(r)

        db_logger.info("Abonelik kart güncelleme cevabı: " + str(r))

        return r
