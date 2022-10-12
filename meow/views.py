from django.shortcuts import render, redirect, HttpResponse

from subscription.models import PricingModel

from django.views.decorators.csrf import csrf_exempt


def index(request):
    pm = PricingModel.objects.filter(pricing_type='0').order_by("order")
    context = {
        "title": "Meow Meow | Kedi Dostlarımıza Kutu Dolu Mutluluk...",
        'pms': pm
    }
    return render(request, "index.html", context)


def mesafeli(request):
    return render(request, 'infos/mesafeli.html')


def teslimatiade(request):
    context = {
        'vis': 'visible'
    }
    return render(request, 'teslimatiade.html', context)


def gizlilikpolitikasi(request):
    context = {
        'vis': 'visible'
    }
    return render(request, 'gizlilikpolitikasi.html', context)


def cerezpolitikasi(request):
    context = {
        'vis': 'visible'
    }
    return render(request, 'cerezpolitikasi.html', context)


@csrf_exempt
def deneme(request):
    print("post", request.POST)
    print("get", request.GET)
    print("headers", request.headers)
    print("body", request.body)
    return HttpResponse("nothing")
