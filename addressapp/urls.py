from django.urls import path, include

from . import views

urlpatterns = [
    path('load-cities', views.load_districts, name="ajax_load_districts"),
]