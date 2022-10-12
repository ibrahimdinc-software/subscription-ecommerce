from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test

# from mail.mailer import say_welcome, password_reset

from .forms import LoginForm, RegisterForm
from .models import User, UserNotification

from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from meow.custom_decorator import user_test

# Create your views here.


@user_test(direction_url="login")
def userLogin(request):
    form = LoginForm(request.POST or None)
    context = {"form": form, "title": "Giriş Yap"}

    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            messages.info(request, "Kullanıcı Adı veya Parola Hatalı")
            return render(request, "user/login.html", context)

        messages.success(request, "Başarıyla Giriş Yaptınız")
        login(request, user)

    if 'next' in request.POST:
        return redirect(request.POST.get('next'))
    elif request.user.is_superuser:
        return redirect("admin:index")
    elif request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "user/login.html", context)


@user_test(direction_url="login")
def register(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
        "title": "Kayıt Ol"
    }
    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        newUser = User(first_name=first_name,
                       last_name=last_name, email=email)
        newUser.set_password(password)
        newUser.save()

        user = authenticate(email=email, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, "Başarıyla kayıt oldunuz")

        from notifications.notification import Notification
        n = Notification(request)
        n.add_notif_user('address', request.user)
        n.add_notif_user('catinfo', request.user)

        # say_welcome(request.user)

    if form['email'].errors or form['password'].errors:
        if form['email'].errors:
            messages.info(request, form['email'].errors[0])
        if form['password'].errors:
            messages.info(request, form['password'].errors[0])
    elif 'next' in request.POST:
        return redirect(request.POST.get('next'))
    elif request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "user/register.html", context=context)


def userLogout(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yapıldı."),
    return redirect("index")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": user.email,
                        "protocol": request.META["HTTP_HOST"],
                        "domain": request.META["SERVER_NAME"],
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                    }
                    # password_reset(c)

                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html", context={"form": password_reset_form})


def emailControl(request):
    email = request.GET.get("email")
    obj = User.objects.filter(email=email).first()
    if obj:
        obj = True
    else:
        obj = False
    return JsonResponse({'obj': obj})
