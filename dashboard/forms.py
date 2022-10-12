from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils.crypto import get_random_string

from phonenumber_field.formfields import PhoneNumberField

from user.models import User
from user.forms import RegisterForm, DeliveryAddressForm

from product.models import CategoryModel, ProductModel

from subscription.models import PricingPlanModel, PricingModel

from mycat.forms import MyCatForm

from paymentapp.forms import PaymentForm, MONTHS, YEARS

# from mail.mailer import say_welcome


class WizardForms(forms.Form):
    pricing = forms.CharField(max_length=100)
    products = forms.ModelMultipleChoiceField(
        queryset=ProductModel.objects.exclude(category=None), required=False)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    email = forms.CharField(max_length=100, required=False)
    phone = PhoneNumberField()
    password = forms.CharField(max_length=100, required=False)
    province = forms.CharField(max_length=100)
    district = forms.CharField(max_length=100)
    first_line = forms.CharField(max_length=100)
    cat_name = forms.CharField(max_length=100, required=False)
    gender = forms.CharField(max_length=100, required=False)
    status = forms.CharField(max_length=100, required=False)
    spec_case = forms.CharField(max_length=300, required=False)
    card_number = forms.CharField(max_length=100)
    full_name = forms.CharField(max_length=100)
    last_usage_month = forms.ChoiceField(choices=MONTHS)
    last_usage_year = forms.ChoiceField(choices=YEARS)
    cvv = forms.CharField(max_length=100)

    def clean(self):
        return self.cleaned_data

    def create(self, request):
        cd = self.clean()
        user = {
            "first_name": cd.get("first_name"),
            "last_name": cd.get("last_name"),
            "email": cd.get("email"),
            "password": cd.get("password"),
            "confirm": cd.get("password"),
            "phone": cd.get("phone")
        }
        address = {
            "province": cd.get("province"),
            "district": cd.get("district"),
            "first_line": cd.get("first_line")
        }
        cat = {
            "user": request.user,
            "name": cd.get("cat_name"),
            "gender": cd.get("gender"),
            "status": cd.get("status"),
            "spec_case": cd.get("spec_case")
        }
        if not request.user.is_authenticated:

            rf = RegisterForm(user)
            if rf.is_valid():
                rf_cd = rf.cleaned_data
                newUser = User(first_name=rf_cd.get("first_name"),
                               last_name=rf_cd.get("last_name"), email=rf_cd.get("email"))
                newUser.set_password(rf_cd.get("password"))
                newUser.save()

                user = authenticate(email=rf_cd.get("email"),
                                    password=rf_cd.get("password"))
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Başarıyla kayıt oldunuz")
                # say_welcome(request.user)

            if rf['email'].errors or rf['password'].errors:
                if rf['email'].errors:
                    messages.info(request, rf['email'].errors[0])
                if rf['password'].errors:
                    messages.info(request, rf['password'].errors[0])

                return ""

        user = request.user
        user.phone = cd.get("phone")
        user.save()

        daf = DeliveryAddressForm(address)
        if user.delivery_default_address:
            daf = DeliveryAddressForm(
                address, instance=user.delivery_default_address)

        if daf.is_valid():
            daf = daf.save(commit=False)
            daf.user = user
            daf.save()

            user.delivery_default_address = daf
            user.save()

        mcf = MyCatForm(cat, user=request.user)

        if mcf.is_valid():
            mcf.save()

        ppm = PricingPlanModel.objects.get(referenceCode=cd.get("pricing"))
        if ppm.pricing.referenceCode == "ozel":
            price = 0
            ps = []
            random_str = get_random_string(length=10)
            if len(cd.get("products")) <= 3:
                price = 15
                ps.append(ProductModel.objects.get(code="kargo"))
            for p in cd.get("products"):
                price += p.price
                ps.append(p)
            pricing = PricingModel.objects.create(
                order=-1,
                name=user.email.split("@")[0] + "-" + random_str,
                code="ozel"+user.email.split("@")[0]+random_str,
                first_price=price,
                discount=0,
                pricing_type="2"
            )

            pricing.products.add(*ps)
            pricing.secondaryProducts.add(*ps)
            pricing.save()

            n_ppm = PricingPlanModel.objects.create(
                name="özel|"+pricing.name,
                interval=ppm.interval,
                frequency=ppm.frequency,
                pricing=pricing
            )
            n_ppm.save()
            cd["pricing"] = n_ppm.referenceCode
