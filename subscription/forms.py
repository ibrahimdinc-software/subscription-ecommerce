from datetime import datetime, timedelta

from django import forms

from .models import CancelSubscription


class CancelSubscriptionForm(forms.ModelForm):
    class Meta:
        model = CancelSubscription
        fields = [
            'user',
            'subscription',
            'is_approved',
            'description'
        ]

    def clean(self):
        user = self.cleaned_data.get("user")
        subscription = self.cleaned_data.get("subscription")
        is_approved = self.cleaned_data.get("is_approved")
        description = self.cleaned_data.get("description")

        cm = CancelSubscription.objects.filter(subscription=subscription)

        if cm:
            self.add_error("__all__",
                           "İptal talebiniz alındı ve onay bekliyor.")

        values = {
            "user": user,
            "subscription": subscription,
            "is_approved": is_approved,
            "description": description
        }
        return values
