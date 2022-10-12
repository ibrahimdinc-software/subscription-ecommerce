import base64
import json

from order.order import Order
from subscription import iyzi

from .serializers import HandShakeSerializer


class Pay:
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def threedgift(self, convId, order, paymentForm, giftForm, req):

        import logging
        logging.basicConfig(filename='threedgift.log', level=logging.DEBUG)

        user = req.user
        request = {
            "locale": "tr",
            "conversationId": str(convId),
            "price": str(order.get_total_price()),
            "paidPrice": str(order.get_total_price()),
            "installment": 1,
            "paymentChannel": "WEB",
            "basketId": str(convId),
            "paymentGroup": "PRODUCT",
            "paymentCard": {
                "cardHolderName": paymentForm.get("full_name"),
                "cardNumber": paymentForm.get("card_number"),
                "expireYear": paymentForm.get("last_usage_year"),
                "expireMonth": paymentForm.get("last_usage_month"),
                "cvc": paymentForm.get("cvv")
            },
            "buyer": {
                "id": str(user.id),
                "name": user.first_name,
                "surname": user.last_name,
                "identityNumber": "11111111111",
                "email": user.email,
                "gsmNumber": str(user.phone),
                "registrationAddress": giftForm.get('first_line'),
                "city": giftForm.get('province'),
                "district": giftForm.get('district'),
                "country": "Turkey",
                "ip": self.get_client_ip(req)
            },
            "shippingAddress": {
                "address": giftForm.get('first_line'),
                "contactName": giftForm.get('name'),
                "city": giftForm.get('province'),
                "district": giftForm.get('district'),
                "country": "Turkey"
            },
            "billingAddress": {
                "address": giftForm.get('first_line'),
                "contactName": giftForm.get('name'),
                "city": giftForm.get('province'),
                "district": giftForm.get('district'),
                "country": "Turkey"
            },

            "currency": "TRY",
            "callbackUrl": "https://meowmeow.com.tr/payment/conversation"  # ! Geri Dönüş
        }

        basketItems = []

        for i in order.get_products():
            basketItems.append({
                "id": str(i.id),
                "price": str(i.price),
                "name": i.name,
                "category1": "Kedi Malzemeleri",
                "category2": "Kedi Malzemeleri",
                "itemType": "PHYSICAL"
            })

        request["basketItems"] = basketItems

        logging.info("request: " + str(request))

        three_d = iyzi.iyzipay.ThreedsInitialize().create(
            request, iyzi.options)

        threed_dict = self.responseJson(three_d.read().decode('utf-8'))

        logging.info("threed_dict: " + str(threed_dict))

        if "errorMessage" in threed_dict:
            return {'status': 'failure', 'message': threed_dict.get("errorMessage")}

        threed_dict['threeDSHtmlContent'] = self.htmlDecode(
            threed_dict.get('threeDSHtmlContent'))

        return threed_dict

    def control(self, request):
        import logging
        logging.basicConfig(filename='control.log',
                            level=logging.DEBUG, filemode="w")

        logging.info("request: " + str(request))
        print(request)

        if request.get('mdStatus') != '1':
            logging.info("request: " + str(request))
            return {'status': 'failure', 'message': 'Doğrulama başarısız oldu.'}
        else:
            return {'status': 'success'}

    def endControl(self, conv, rp):
        # sakla dediği veriler burada saklanacak
        if rp.get('status') == 'success':

            conv.is_pay = True
            conv.save()

            HandShakeSerializer().create(validated_data=rp)

            return {'status': 'success'}
        else:
            return {'status': 'failure', 'message': rp.get('errorMessage')}

    def handshake(self, conv):
        request = {
            "locale": "tr",
            "conversationId": conv.conversationId,
            "paymentId": conv.paymentId
        }

        if conv.conversationData:
            request["conversationData"] = conv.conversationData

        res = iyzi.iyzipay.ThreedsPayment().create(request, iyzi.options)
        res = self.responseJson(res.read().decode('utf-8'))

        return self.endControl(conv, res)

    def payment_control(self, paymentId):
        request = {
            'locale': 'tr',
            'paymentId': paymentId
        }
        payment = iyzi.iyzipay.Payment().retrieve(request, iyzi.options)

        return self.responseJson(payment.read().decode('utf-8'))

    def retrieve_cards(self):
        request = {
            "locale": "TR",
            "conversationId": "1"
        }

        rc = iyzi.iyzipay.CardList().retrieve(request, iyzi.options)
        print(rc.read().decode('utf-8'))

    def htmlDecode(self, html):
        return base64.b64decode(html)

    def responseJson(self, response):
        return json.loads(response)
