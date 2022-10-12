from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SurveyForm
from .models import InfoSurvey
# Create your views here.


def survey(request):
    form = SurveyForm(request.POST or None)

    participant = InfoSurvey.objects.all().count()

    if form.is_valid():
        f = form.save()
        messages.info(request, "Kaydınız başarıyla tamamlanmıştır. Meow!")
        return redirect(survey)
    elif form.is_valid() == False and form.errors:
        messages.info(
            request, "Kaydınız daha önce alınmıştır. İlginiz için teşekkürler. Meow!")
        return redirect(survey)

    context = {
        "form": form,
        "participant": participant
    }

    return render(request, "survey/survey.html", context)
