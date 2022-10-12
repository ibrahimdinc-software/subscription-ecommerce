from .notification import Notification

def notification(request):
    if request.user.is_authenticated:
        return{"notification": Notification(request)}
    return {}