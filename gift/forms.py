from django import forms

from .models import GiftModel


class GiftForm(forms.ModelForm):
    class Meta:
        model = GiftModel
        fields = [
            'catname',
            'name',
            'phone',
            'province',
            'district',
            'first_line',
            'spec_case',
            'want_bag',
            'spec_note',
        ]

    def clean(self):
        cd = self.cleaned_data

        if len(cd.get("name")) < 5:
            self.add_error("name", "Geçersiz formata sahip bir isim girdiniz.")

        if not cd.get("phone"):
            self.errors.pop("phone")
            self.add_error("phone", "Eksik numara bilgisi girdiniz.")
        elif len(cd.get("phone")) < 13:
            self.add_error("phone", "Eksik numara bilgisi girdiniz.")

        if len(cd.get("first_line")) < 5:
            self.add_error("first_line", "Eksik bilgi girdiniz.")

        return cd
