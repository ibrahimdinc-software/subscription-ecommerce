from django import forms

from .models import User, DeliveryAddress


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ["province",
                  "district", "first_line"]


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-Posta")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="İsim")
    last_name = forms.CharField(max_length=50, label="Soyisim")
    email = forms.CharField(max_length=50, label="E-posta")
    password = forms.CharField(
        max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(
        max_length=20, label="Parolayı Doğrula", widget=forms.PasswordInput)

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            self._errors["password"] = ["Parolalar eşleşmiyor."]
        if User.objects.filter(email=email).exists():
            self._errors["email"] = [
                "Bu e-posta adresi daha önce kullanılmış."]
        values = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "confirm": confirm,
            "is_registered": True
        }
        return values


class UserSettingsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label="İsim")
    last_name = forms.CharField(max_length=50, label="Soyisim")
    email = forms.CharField(max_length=50, label="E-Posta")
    phone = forms.CharField(max_length=16, label="Telefon Numarası")

    def clean(self):
        cleaned_data = self.cleaned_data
        if 'email' in self.changed_data and User.objects.filter(email=cleaned_data.get("email")).exists():
            raise forms.ValidationError(
                "Bu email adresi başka bir kullanıcı tarafından kullanılıyor.")
        return cleaned_data

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone"
        ]


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        max_length=20, label="Mevcut Parola", widget=forms.PasswordInput)
    npassword = forms.CharField(
        max_length=20, label="Yeni Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(
        max_length=20, label="Yeni Parolayı Doğrula", widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get("password")
        npassword = self.cleaned_data.get("npassword")
        confirm = self.cleaned_data.get("confirm")

        if password and npassword and confirm and npassword != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        values = {
            "npassword": npassword,
            "confirm": confirm,
            "password": password
        }
        return values
