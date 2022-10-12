from django.urls import path, include

from . import views

urlpatterns = [
    path("newcard", views.newcard, name="newcard"),
    path("newcardsuccess", views.newcardsuccess, name="newcardsuccess"),
    path("newcardreturn", views.newcardreturn, name="newcardreturn"),
]
