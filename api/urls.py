from django.urls import path

from . import views

urlpatterns = [
    path('orderStatus/', views.OrderStatusGenericView.as_view()),
    path('paymentMethods/', views.PaymentMethodsGenericView.as_view()),
    path('orders/', views.OrdersGenericView.as_view()),
    path('orderDetails/', views.OrderDetailsGenericView.as_view()),
]
