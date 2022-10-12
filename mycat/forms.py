from django import forms
from django.core.files import File

from .models import MyCatModel

from PIL import Image
import time


class MyCatForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = MyCatModel
        fields = [
            "id",
            "name",
            "picture",
            "gender",
            "status",
            "spec_case",
            'x', 'y', 'width', 'height',
        ]

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(MyCatForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data
        if cd.get("picture") == False:
            cd["picture"] = "None"
        if not cd.get("picture") and not cd.get("id"):
            cd["picture"] = None
        return cd

    def save(self, commit=True):
        cat = super(MyCatForm, self).save(commit=False)

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        id = self.cleaned_data.get('id')

        if id:
            cat = MyCatModel.objects.get(id=id)

            c = self.clean()

            cat.name = c.get("name")
            cat.gender = c.get("gender")
            cat.status = c.get("status")
            cat.spec_case = c.get("spec_case")

            if c.get("picture"):
                if c.get("picture") == "None":
                    cat.picture = None
                else:
                    if cat.picture:
                        cat.picture.delete()
                    cat.picture = c.get("picture")

            cat.save()
        else:

            cat.user = self._user

            cat.save()

        if self.cleaned_data.get("picture") != "None" and self.cleaned_data.get("picture"):

            image = Image.open(cat.picture)
            cropped_image = image.crop((x, y, w+x, h+y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(cat.picture.path)

        return cat
