from django.urls import path


from . import views

urlpatterns = [
    path('conversation', views.ConversationGenericView.as_view()),
]
