from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.template.loader import get_template

from .models import MyCatModel
from .forms import MyCatForm

# Create your views here.
import logging
db_logger = logging.getLogger('db')


def instanceForm(request):
    form = MyCatForm(request.POST or None,
                     request.FILES or None, user=request.user)
    if request.GET.get("cat_id"):
        mCat = MyCatModel.objects.get(id=request.GET.get("cat_id"))
        form = MyCatForm(instance=mCat, user=request.user)

    return render(request, "mycat/catForm.html", {'form': form})


def deleteCat(request, id):
    db_logger.info(request.user.email + ' ' + str(id) + ' nolu kediyi sildi.')
    mc = MyCatModel.objects.get(id=id)
    mc.delete()
    return redirect("mycat")
