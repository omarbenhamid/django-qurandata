''' 
Created on 5 avr. 2018

@author: omar
'''
from django.urls.conf import path
from . import views
from datetime import date
from django.shortcuts import redirect
from django.http.response import HttpResponse

urlpatterns = [path('', lambda r: HttpResponse("404",status=404), name='qurandata_api_root'),
                path('sura/<int:suraidx>/aya/<int:ayaidx>/text', 
                    views.get_aya_text, name='get_aya_text'),
                path('sura/<int:suraidx>/aya/<int:ayaidx>/info', 
                    views.get_aya_info, name='get_aya_info')]