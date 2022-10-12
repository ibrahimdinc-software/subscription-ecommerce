from django.shortcuts import render, redirect
from django.contrib import messages

from rest_framework import generics
from rest_framework import mixins


from .serializers import ConversationSerializer, HandShakeSerializer
from .models import Conversation,  HandShake

from .payment import Pay

from order.models import OrderModel

# Create your views here.
import logging
db_logger = logging.getLogger('db')


class ConversationGenericView(generics.GenericAPIView, mixins.CreateModelMixin):

    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()

    def get_object(self, conversationId):
        return self.queryset.get(conversationId=conversationId)

    def get(self, request):

        db_logger.info(request.user.email + ' ödeme geri dönüş')

        pay = Pay()
        pc = pay.control(request.data)

        if pc.get("status") == "failure":
            db_logger.error(request.user.email +
                            ' ödeme geri dönüş hata: ' + pc.get("message"))
            messages.info(request, pc.get("message"))
            om = OrderModel.objects.filter(
                id=int(request.data.get("conversationId"))).first()
            if om:
                om.delete()
                db_logger.error(request.user.email +
                                ' ödeme geri dönüş hatadan dolayı sipariş silindi.')
            return redirect("gift")

        r = self.create(request)
        obj = self.get_object(r.data['conversationId'])

        db_logger.info(request.user.email +
                       ' ödeme geri dönüş conversation oluştu. id: ' + str(r.data['conversationId']))

        ph = pay.handshake(obj)

        db_logger.info(request.user.email +
                       ' ödeme geri dönüş handshake')

        if ph.get('status') == 'failure':
            db_logger.error(request.user.email +
                            ' ödeme geri dönüş handshake hata: ' + pc.get("message"))
            messages.info(request, pc.get("message"))
            return redirect("gift")

        db_logger.info(request.user.email +
                       ' ödeme geri dönüş başarılı')
        return render(request, "paymentapp/success.html")

    def post(self, request):

        db_logger.info(request.user.email + ' ödeme geri dönüş')

        pay = Pay()
        pc = pay.control(request.data)

        if pc.get("status") == "failure":
            db_logger.error(request.user.email +
                            ' ödeme geri dönüş hata: ' + pc.get("message"))
            messages.info(request, pc.get("message"))
            om = OrderModel.objects.filter(
                id=int(request.data.get("conversationId"))).first()
            if om:
                om.delete()
                db_logger.error(request.user.email +
                                ' ödeme geri dönüş hatadan dolayı sipariş silindi.')
            return redirect("gift")

        r = self.create(request)
        obj = self.get_object(r.data['conversationId'])

        db_logger.info(request.user.email +
                       ' ödeme geri dönüş conversation oluştu. id: ' + str(r.data['conversationId']))

        ph = pay.handshake(obj)

        db_logger.info(request.user.email +
                       ' ödeme geri dönüş handshake')

        if ph.get('status') == 'failure':
            db_logger.error(request.user.email +
                            ' ödeme geri dönüş handshake hata: ' + pc.get("message"))
            messages.info(request, pc.get("message"))
            return redirect("gift")

        db_logger.info(request.user.email +
                       ' ödeme geri dönüş başarılı')
        return render(request, "paymentapp/success.html")
