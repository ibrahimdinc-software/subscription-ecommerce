from django import forms

from .models import OrderCancelModel, OrderModel


class OrderCancelForm(forms.ModelForm):
    class Meta:
        model = OrderCancelModel
        fields = [
            'order',
            'status'
        ]

    def save(self, *args, **kwargs):
        f = super(OrderCancelForm, self).save(
            commit=False)  # Call the real save() method
        o = f.order
        print(o)
        o.status = '20'
        print(o.status)

        o.save()
        print(o, o.status)

        f.save()
