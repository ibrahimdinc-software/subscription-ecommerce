from django.urls import path, include

from . import views

urlpatterns = [
    path('instanceForm', views.instanceForm,
         name="instanceForm"),
    path('deletecat/<int:id>', views.deleteCat,
         name="deletecat"),
]
