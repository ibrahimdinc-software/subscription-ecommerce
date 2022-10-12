from django.shortcuts import render

from .notification import Notification

# Create your views here.

def get_old(request):
    n = Notification(request)
    old_notifs = n.get_old_notifs()
    return render(request, "notifications/old-notifications.html", {"old_notifs":old_notifs})