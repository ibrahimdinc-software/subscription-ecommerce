"""meow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static as s
from django.views.generic import RedirectView
from django.templatetags.static import static


from . import views

urlpatterns = [
    path('bosswindow/', admin.site.urls, name="admin"),
    path('', views.index, name="index"),
    path('dashboard/', include("dashboard.urls"), name="dashboard"),
    path('addressapp/', include("addressapp.urls")),
    path('subscription/', include("subscription.urls")),
    path('', include("user.urls")),
    path('notifications/', include("notifications.urls")),
    path('mycat/', include("mycat.urls")),
    path('payment/', include("paymentapp.urls")),
    path('api/', include("api.urls")),
    # path("messages/", include("pinax.messages.urls", namespace="pinax_messages")),


    path('favicon.ico/',
         RedirectView.as_view(url=static("images/favicon.ico")), name="favicon"),
    path('mesafelisatis', views.mesafeli, name='mesafeli'),
    path('cerezpolitikasi', views.cerezpolitikasi, name="cerezpolitikasi"),
    path('teslimatiade', views.teslimatiade, name="teslimatiade"),
    path('gizlilikpolitikasi', views.gizlilikpolitikasi, name="gizlilikpolitikasi"),
    path('deneme', views.deneme, name="deneme"),
]
if settings.DEBUG:
    urlpatterns += s(settings.MEDIA_URL,
                     document_root=settings.MEDIA_ROOT)
