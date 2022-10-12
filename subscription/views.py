from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from order.models import OrderModel
from . import iyzic


import logging
db_logger = logging.getLogger('db')


def newcard(request):
    r = iyzic.Subscription().cardUpdate(request.user.sub.referenceCode)
    db_logger.info(request.user.email + ' yeni kart ekleme.')
    return HttpResponse(r.get("checkoutFormContent"))


@csrf_exempt
def newcardsuccess(request):

    db_logger.info(request.user.email + ' newcardsuccess.' + str(request.POST))

    return redirect("newcardreturn")


def newcardreturn(request):
    order = OrderModel.objects.filter(subscription=request.user.sub).last()

    db_logger.info(request.user.email + ' yeni kart ekleme başarılı.')

    order.retry_count = 0
    order.retry_message = "El ile sıfırlama. Yeni kart eklendi."
    order.save()
    iyzic.Subscription(request.user.sub.referenceCode).retry(order)
    messages.info(request, "Kartınız başarıyla güncellenmiştir.")
    return redirect("subscription")
