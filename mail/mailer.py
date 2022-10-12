
from mailer import send_mail, send_html_mail
from django.conf import settings
from django.template import loader


def say_welcome(user):
    context = {
        'name': user.first_name + ' ' + user.last_name
    }

    template = loader.get_template('mail/welcome-mail.html').render(context)

    send_html_mail("Meow Meow'a Hoşgeldin", 'Mail düzgün görüntülenmiyorsa tıklayın.', template,
                   settings.EMAIL_HOST_USER, [user.email],)


def password_reset(context):

    template = loader.get_template(
        'registration/password_reset_email.html').render(context)

    send_html_mail("Meow Meow Şifre Sıfırlama Talebi", 'Mail düzgün görüntülenmiyorsa tıklayın.', template,
                   settings.EMAIL_HOST_USER, [context["email"]],)
