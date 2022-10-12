from django.urls import path, include

from . import views

urlpatterns = [
    path('get-old-notifications', views.get_old, name="get-old"),
]