from django.conf import settings
from django.forms.models import model_to_dict

from datetime import datetime, timedelta

from user.models import UserNotification

from .models import Notification as mNotif
from .models import Notification_Subject


class Notification(object):

    def __init__(self, request=None):
        if request:
            self.notif = UserNotification.objects.filter(user=request.user)
            self.unread = self.get_unread()

    def get_unread(self):
        unread = {
            "Bildirim": 0,
            "Profil": 0,
            "Kedi": 0,
            "Hediye": 0,
            "Oylama": 0,
            "Abonelik": 0
        }
        for n in self.notif:
            if not n.is_read:
                n = n.notification
                unread[n.subject.name] += 1
        return unread

    def add_notif_user(self, code, user, message=None):
        un = None
        if not message:
            notif = self.get_notification(code)
            un = UserNotification(
                notification=notif, user=user, time=datetime.now())
        else:
            ns = Notification_Subject.objects.get(name='Abonelik')
            notif = mNotif(name='Abonelik İptali', content=message,
                           subject=ns, code=message, time=datetime.now())
            notif.save()
            un = UserNotification(
                notification=notif, user=user, time=datetime.now())
        un.save()

    def get_notification(self, code):
        notif = mNotif.objects.get(code=code)
        return notif

    def get_notifs_for_view(self, subject):
        if subject == "all":
            time_threshold = datetime.now() - timedelta(days=30)
            notifs = self.notif.order_by(
                "-time").filter(time__gte=time_threshold)
            self.read(notifs)
            return notifs
        if self.unread.get(subject) > 0:
            notifs = self.notif.filter(notification__subject__name=subject).filter(
                is_read=0).order_by("-time")
            self.read(notifs)
            return notifs

    def get_old_notifs(self):
        time_threshold = datetime.now() - timedelta(days=30)
        notifs = self.notif.filter(time__lt=time_threshold)
        return notifs

    def has_old_notifs(self):
        time_threshold = datetime.now() - timedelta(days=30)
        notifs = self.notif.filter(time__lt=time_threshold)
        if notifs:
            return True
        return False

    def read(self, notifications):
        for n in notifications:
            n.is_read = True
            n.save()
