import json
from datetime import datetime

from django import forms

from subscription import iyzi


MONTHS = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
]

YEARS = [
    ("2020", "2020"),
    ("2021", "2021"),
    ("2022", "2022"),
    ("2023", "2023"),
    ("2024", "2024"),
    ("2025", "2025"),
    ("2026", "2026"),
    ("2027", "2027"),
    ("2028", "2028"),
    ("2029", "2029"),
    ("2030", "2030"),
    ("2031", "2031"),
    ("2032", "2032"),
    ("2033", "2033"),
    ("2034", "2034"),
    ("2035", "2035"),
]


class PaymentForm(forms.Form):
    pricing = forms.CharField(max_length=60)
    full_name = forms.CharField(max_length=50)
    card_number = forms.CharField(
        max_length=19, min_length=19)
    last_usage_month = forms.ChoiceField(choices=MONTHS)
    last_usage_year = forms.ChoiceField(choices=YEARS)
    cvv = forms.CharField(max_length=3)

    def clean(self):
        pricing = self.cleaned_data.get("pricing")
        full_name = self.cleaned_data.get("full_name")
        card_number = self.cleaned_data.get("card_number")
        last_usage_month = self.cleaned_data.get("last_usage_month")
        last_usage_year = self.cleaned_data.get("last_usage_year")
        cvv = self.cleaned_data.get("cvv")

        card_number = card_number.replace('-', '')
        card_number = card_number.replace('_', '')

        if len(card_number) > 16 or len(card_number) < 16:
            self.add_error("card_number",
                           "Kart numarası eksik veya hatalı.")
        if len(full_name) < 5:
            self.add_error(
                "full_name", "Kart üzerindeki isim eksik veya hatalı.")
        if int(last_usage_year) <= datetime.now().year:
            if int(last_usage_month) < datetime.now().month:
                self.add_error("last_usage_month",
                               "Son kullanma tarihi geçmiş bir kart kullandınız.")

        if len(cvv) < 3 or len(cvv) > 4:
            self.add_error(
                "cvv", "Kart güvenlik numarasını eksik veya hatalı girdiniz.")

        values = {
            "pricing": pricing,
            "full_name": full_name,
            "card_number": card_number,
            "last_usage_month": last_usage_month,
            "last_usage_year": last_usage_year,
            "cvv": cvv
        }
        return values

    def get_errors(self):
        errors = {}
        for e in self.errors.as_data():
            error = self.errors.as_data()
            if e == "__all__":
                errors["paymentForm"] = error[e][0].message
            else:
                errors[e] = error[e][0].message
        return errors

    def create_subscription(self, user):
        cd = self.cleaned_data
        r = iyzi.Subscription().api(request={
            'pricingPlanReferenceCode': cd.get('pricing'),
            'subscriptionInitialStatus': 'ACTIVE',
            'paymentCard': {
                'cardHolderName': cd.get('full_name'),
                'cardNumber': cd.get('card_number'),
                'expireYear': cd.get('last_usage_year'),
                'expireMonth': cd.get('last_usage_month'),
                'cvc': cd.get('cvv'),
                'registerConsumerCard': True
            },
            'customer': {
                'name': user.first_name,
                'surname': user.last_name,
                'email': user.email,
                'gsmNumber': str(user.phone),
                'identityNumber': '11111111111',
                'billingAddress': {
                    'contactName': user.get_full_name(),
                    'city': user.delivery_default_address.province,
                    'country': 'Türkiye',
                    'address': user.delivery_default_address.first_line
                },
                'shippingAddress': {
                    'contactName': user.get_full_name(),
                    'city': user.delivery_default_address.province,
                    'country': 'Türkiye',
                    'address': user.delivery_default_address.first_line
                }

            }
        }, foptions=iyzi.options)
        r = json.loads(r.read().decode('utf-8'))
        return r
