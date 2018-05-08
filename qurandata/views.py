from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse, JsonResponse
from .models import Aya

# Create your views here.

def get_aya_text(request, suraidx, ayaidx):
    aya = get_object_or_404(Aya,
        sura__index = suraidx,
        index = ayaidx)
    return HttpResponse(aya.text)

def get_aya_info(request, suraidx, ayaidx):
    aya = get_object_or_404(Aya,
        sura__index = suraidx,
        index = ayaidx)
    return JsonResponse({
            "index":ayaidx,
            "text":aya.text,
            "url": aya.get_url(),
            "sura": {
                "title": aya.sura.name,
                "index": aya.sura.index,
                "ayacount": aya.sura.ayas
            }
        })
