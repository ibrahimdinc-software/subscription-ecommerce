from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test

from notifications.notification import Notification as N
from notifications.models import Notification

from user.models import UserNotification, User, DeliveryAddress
from user.forms import UserSettingsForm, DeliveryAddressForm, PasswordResetForm

from subscription.forms import CancelSubscriptionForm
from subscription.models import PricingPlanModel, PricingModel, SubscriptionModel, CancelSubscription
from subscription import iyzic

from order.order import Order
from order.models import OrderModel, OrderCancelModel
from order.forms import OrderCancelForm

from product.models import CategoryModel

from mycat.models import MyCatModel
from mycat.forms import MyCatForm

from gift.forms import GiftForm
from gift.models import GiftModel
from product.models import ProductModel

from paymentapp.forms import PaymentForm
from paymentapp.payment import Pay

from .forms import WizardForms

import logging
db_logger = logging.getLogger('db')
# Create your views here.


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def dashboard(request):
    db_logger.info(request.user.email + ' Kontrol Panelinde')
    notification = N(request)
    unread = notification.get_unread()
    context = {
        "unread": unread
    }
    return render(request, "dashboard/dashboard.html", context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def notifications(request):
    db_logger.info(request.user.email + ' Bildirim Ekranında')
    notification = N(request)
    notifs = notification.get_notifs_for_view("all")
    context = {
        "notifs": notifs
    }
    return render(request, "dashboard/notifications.html", context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def profile(request):
    db_logger.info(request.user.email + ' Profil Ekranında')
    notifs = N(request).get_notifs_for_view("Profil")

    delAddress = request.user.delivery_default_address

    if delAddress:
        addressForm = DeliveryAddressForm(instance=delAddress)
    else:
        addressForm = DeliveryAddressForm()

    settingsForm = UserSettingsForm(instance=request.user)
    passwordResetForm = PasswordResetForm(request.POST or None)

    errors = {}
    context = {
        "notifs": notifs,
        "settingsForm": settingsForm,
        "addressForm": addressForm,
        "passwordResetForm": passwordResetForm,
        "errors": errors
    }

    if request.POST and "saveSettingsForm" in request.POST:
        settingsForm = UserSettingsForm(
            request.POST or None, instance=request.user)
        addressForm = DeliveryAddressForm(
            request.POST or None, instance=delAddress)

        if settingsForm.is_valid() and addressForm.is_valid():
            db_logger.info(request.user.email +
                           ' Bilgileri Düzenle Panelinde değişiklik yaptı.')
            form = settingsForm.save()

            f = addressForm.save(commit=False)
            f.user = request.user
            f.save()
            messages.info(
                request, "Güncelleme işlemi başarıyla gerçekleştirildi.")
            return redirect(profile)

        elif settingsForm.errors.as_data() or addressForm.errors.as_data():
            for e in settingsForm.errors.as_data():
                error = settingsForm.errors.as_data()
                if e == "__all__":
                    errors["userForm"] = error[e][0].message
                else:
                    errors[e] = error[e][0].message
            for e in addressForm.errors.as_data():
                error = addressForm.errors.as_data()
                if e == "__all__":
                    errors["addressForm"] = error[e][0].message
                else:
                    errors[e] = error[e][0].message

            db_logger.warning(request.user.email +
                              ' Bilgileri Düzenle Panelinde değişiklik yaptı. ' + 'Hata aldı: ' + str(errors))

    elif request.POST and "changePassword" in request.POST:
        if passwordResetForm.is_valid():
            db_logger.info(request.user.email +
                           ' Şifre Değiştir Panelinde değişiklik yaptı.')
            user = User.objects.get(email=request.user)
            opass = passwordResetForm.cleaned_data.get("password")
            npass = passwordResetForm.cleaned_data.get("npassword")
            us = authenticate(email=request.user.email, password=opass)
            if us:
                user.set_password(npass)
                user.save()
                login(request, user)
                messages.info(request, "Şifre başarıyla güncellendi.")
            else:
                db_logger.info(request.user.email +
                               ' Şifre Değiştir Panelinde hatalı şifre girdi.')
                messages.info(request, "Mevcut şifrenizi hatalı girdiniz.")
            return redirect(profile)
        elif passwordResetForm.errors.as_data():
            for e in passwordResetForm.errors.as_data():
                error = passwordResetForm.errors.as_data()
                if e == "__all__":
                    errors["passwordResetForm"] = error[e][0].message
                else:
                    errors[e] = error[e][0].message
            db_logger.warning(request.user.email +
                              ' Şifre Değiştir Panelinde değişiklik yaptı.' + ' Hata aldı: ' + 'Hata aldı: ' + str(errors))

    return render(request, "dashboard/profile.html", context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def mycat(request):
    db_logger.info(request.user.email + ' Kedim sayfasında.')
    notifs = N(request).get_notifs_for_view("Kedi")

    cats = MyCatModel.objects.filter(user=request.user)

    catForm = MyCatForm(request.POST or None,
                        request.FILES or None, user=request.user)

    if catForm.is_valid():
        db_logger.info(request.user.email +
                       ' Kedim sayfasında değişiklik yaptı.')
        catForm.save()
        return redirect(mycat)

    context = {
        "notifs": notifs,
        "cats": cats,
        "catForm": catForm
    }

    return render(request, "dashboard/mycat.html", context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def gift(request):
    db_logger.info(request.user.email + ' Hediye sayfasında.')
    notifs = N(request).get_notifs_for_view("Hediye")

    pricing = PricingModel.objects.filter(pricing_type="1").first()

    paymentForm = PaymentForm(request.POST or None)
    giftForm = GiftForm(request.POST or None)

    gift = GiftModel.objects.filter(user=request.user).order_by('-pk')

    formError = {}
    if request.POST:
        r = request.POST
        if giftForm.is_valid():
            db_logger.info(request.user.email +
                           ' hediye sayfasında satın alım yapıyor.')

            cd = giftForm.cleaned_data
            logging.info("cd: " + str(cd))

            order = Order(request)

            products = ProductModel.objects.all()

            if cd.get("want_bag") == "true":
                order.add(products.get(code="bez-canta"))
            if cd.get("spec_note"):
                order.add(products.get(code="kartvizit"))

            for p in pricing.products.all():
                order.add(p)

            if paymentForm.is_valid():
                db_logger.info(request.user.email +
                               ' hediye sayfasında ödeme formu başarılı.')
                f = paymentForm.clean()

                o = order.create_order()

                giftForm = giftForm.save(commit=False)
                giftForm.user = request.user
                giftForm.order = o
                giftForm = giftForm.save()

                pay_start = Pay().threedgift(
                    convId=o.id,
                    order=order,
                    paymentForm=f,
                    giftForm=cd,
                    req=request
                )

                logging.info("pay_start: " + str(pay_start))

                if pay_start["status"] == "failure":
                    o.delete()
                    db_logger.info(request.user.email +
                                   ' hediye sayfasında ödeme hatası: ' + pay_start["message"])
                    messages.info(request, pay_start["message"])
                else:
                    return HttpResponse(pay_start.get("threeDSHtmlContent"))

            else:
                formError = paymentForm.get_errors()
                db_logger.info(request.user.email +
                               ' hediye sayfasında hata aldı: ' + str(formError))
        else:
            formError = giftForm._errors
            db_logger.info(request.user.email +
                           ' hediye sayfasında "Hatalı bilgi var." hatası aldo: ' + str(formError))
            messages.info(request, "Hatalı bilgi var.")

    context = {
        "notifs": notifs,
        "pricing": pricing,
        "paymentForm": paymentForm,
        "giftForm": giftForm,
        "formError": formError,
        "gift": gift,
    }

    return render(request, "dashboard/gift.html", context=context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def voting(request):
    notifs = N(request).get_notifs_for_view("Oylama")
    context = {
        "notifs": notifs,
        "gift": gift
    }
    return render(request, "dashboard/voting.html", context)


def subscript(request):

    notifs = None
    cats = None
    s = None
    categories = CategoryModel.objects.all()

    wf = WizardForms(request.POST or None)

    x = []
    pricings = PricingModel.objects.filter(
        pricing_type="0").order_by("order")
    pricingPlans = PricingPlanModel.objects.all()
    for p in pricings:
        x.append([p, pricingPlans.filter(pricing=p)])

    if request.user.is_authenticated:
        db_logger.info(request.user.email + ' Yeni Abonelik sayfasında.')

        # YöNLENDİRME
        if request.user.sub:
            s = request.user.sub
            if s.status == "1":
                db_logger.info(request.user.email +
                               ' Zaten abone olduğu için yönlendirildi.')
                return asubcription(request)
        # YöNLENDİRME SON

        n = N(request)  # Bildirim
        notifs = n.get_notifs_for_view("Abonelik")

        # FORM TANIMLAMA
        cats = MyCatModel.objects.filter(user=request.user)
        if request.user.delivery_default_address:

            wf = WizardForms(
                request.POST or None,
                initial={
                    'province': request.user.delivery_default_address.province,
                    'district': request.user.delivery_default_address.district,
                    'first_line': request.user.delivery_default_address.first_line,
                    'phone': str(request.user.phone)
                }
            )
        # FORM TANIMLAMA SON

    if wf.is_valid():
        wf.create(request)
        wf_cd = wf.clean()
        paymentForm = PaymentForm(
            {
                'pricing': wf_cd.get('pricing'),
                'full_name': wf_cd.get('full_name'),
                'card_number': wf_cd.get('card_number'),
                'last_usage_month': wf_cd.get('last_usage_month'),
                'last_usage_year': wf_cd.get('last_usage_year'),
                'cvv': wf_cd.get('cvv')
            } or None)

        if paymentForm.is_valid():
            db_logger.info(request.user.email +
                           ' Yeni Abonelik sayfasında ödeme formu başarılı.')
            res = paymentForm.create_subscription(request.user)
            if res.get('status') == 'failure':
                db_logger.info(request.user.email +
                               ' Yeni Abonelik sayfasında hata aldı iyzico dönen cevap: ' + res.get("errorMessage"))
                messages.info(request, res.get("errorMessage"))
                return redirect(subscript)
            else:
                db_logger.info(request.user.email +
                               ' Yeni Abonelik başarıyla oluşturulmuştur.')

                messages.info(request, "Abonelik başarıyla oluşturulmuştur.")
                cd = paymentForm.cleaned_data
                pp = pricingPlans.get(referenceCode=cd.get("pricing"))
                if s:
                    db_logger.info(request.user.email +
                                   ' Yeni Abonelik sayfasında pasif durumdan aktife geçiyor.')
                    s.pricing = pp
                    s.status = "1"
                    s.price = pp.pricing.first_price
                    s.discount = pp.pricing.discount
                    s.referenceCode = res.get("data").get("referenceCode")
                    s.save()
                else:
                    db_logger.info(request.user.email +
                                   ' Yeni Abonelik sayfasında yeni abonelik oluşturuluyor.')
                    sub = SubscriptionModel(
                        user=request.user,
                        pricing=pp,
                        price=pp.pricing.first_price,
                        status="1",
                        discount=pp.pricing.discount,
                        referenceCode=res.get("data").get("referenceCode")
                    )
                    sub.save()
                    request.user.sub = sub
                    request.user.save()

                order = OrderModel(
                    user=request.user,
                    price=pp.pricing.get_discount_price(),
                    subscription=request.user.sub,
                    payment=False,
                    order_type="0",
                    status="0"
                )
                order.save()
                order.products.set(pp.pricing.products.all())
                order.save()
                db_logger.info(request.user.email +
                               ' Yeni Abonelik sayfasında ' + str(order.id) + ' nolu sipariş oluşuyor.')

                iyzisubcontrol = iyzic.Subscription(
                    referenceCode=request.user.sub.referenceCode)
                iyzisubcontrol.create_conversation(order)

                return redirect(subscript)
        else:
            db_logger.info(request.user.email +
                           ' Yeni Abonelik sayfasında hata aldı: ' + str(paymentForm.get_errors()))
            return redirect(subscript)

    context = {
        "notifs": notifs,
        "cats": cats,
        "wf": wf,
        "pricings": x,
        "categories": categories
    }
    return render(request, "dashboard/subscription.html", context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def asubcription(request):
    db_logger.info(request.user.email +
                   ' Abonelik sayfasında.')

    order = OrderModel.objects.filter(
        user=request.user, order_type="0").last()

    sub = request.user.sub

    cancel = CancelSubscription.objects.filter(subscription=sub)

    if "cancel" in request.POST:
        db_logger.info(request.user.email +
                       ' Abonelik sayfasında abonelik iptal talebinde bulundu.')
        cs = CancelSubscriptionForm(
            data={"user": request.user, "subscription": sub, "is_approved": "0"})
        if cs.is_valid():
            cs.save()
            messages.info(request, "İptal talebiniz alındı ve onay bekliyor.")
            return redirect(subscript)
        messages.info(request, cs._errors.as_data()["__all__"][0].message)
        return redirect(subscript)

    context = {
        "sub": sub,
        "cancel": cancel,
        "order": order
    }
    return render(request, "dashboard/asubscription.html", context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def orders(request):
    db_logger.info(request.user.email +
                   ' Siparişler sayfasında.')
    orders = OrderModel.objects.filter(user=request.user).order_by("-date")

    if "cancel" in request.POST:
        oc = OrderCancelForm(
            data={'order': orders.get(id=request.POST.get("id")), 'status': '0'})

        if oc.is_valid():
            oc.save()
            db_logger.info(request.user.email + ' Siparişler sayfasında.' +
                           str(request.POST.get("id")) + ' nolu siparişi iptal ediyor.')
    context = {
        "orders": orders
    }
    return render(request, "dashboard/orders.html", context)


@user_passes_test(lambda u: u.is_authenticated, login_url="register")
def orderCancel(request, id):
    db_logger.info(request.user.email + ' Sipariş iptal sayfasında.' +
                   str(id) + ' nolu siparişin iptalini kontrol ediyor.')
    ocm = OrderCancelModel.objects.get(order=id)

    if 'ok' in request.POST:
        ocm.status = '1'
        db_logger.info(request.user.email + ' Sipariş iptal sayfasında. ' +
                       str(id)+' nolu siparişi kargoya verdi.')
        ocm.save()
        return redirect(orderCancel, id)

    context = {
        'ocm': ocm
    }
    return render(request, "dashboard/cancelOrder.html", context=context)
