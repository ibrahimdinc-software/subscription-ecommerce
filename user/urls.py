from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("login/", views.userLogin, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.userLogout, name="logout"),
    path("emailControl", views.emailControl, name="emailControl"),

    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    #path('', include('django.contrib.auth.urls')),
]
