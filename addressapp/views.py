from .addressing import Address
from django.shortcuts import render

# Create your views here.


def load_districts(request):
    province_id = request.GET.get("province")
    districts = Address().distWid(province_id)
    selected = request.GET.get("selected")

    return render(request, 'addressapp/district_dropdown_list_options.html', {"districts": districts, "selected": selected})
