from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("notifications", views.notifications, name="notifications"),
    path("profile", views.profile, name="profile"),
    path("mycat", views.mycat, name="mycat"),
    path("gift", views.gift, name="gift"),
    path("voting", views.voting, name="voting"),
    path("subscription", views.subscript, name="subscription"),
    path("orders", views.orders, name="orders"),
    path("orderCancel/<int:id>", views.orderCancel, name="orderCancel"),
]
