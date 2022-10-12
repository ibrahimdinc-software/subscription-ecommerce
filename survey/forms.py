from django import forms

from .models import InfoSurvey


class SurveyForm(forms.ModelForm):
    class Meta:
        model = InfoSurvey
        fields = [
            "full_name",
            "email",
            "phone"
        ]
