"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from mains.views import (home_view,
                         about_view,
                         birthday_view,
                         marriage_view,
                         new_year_view,
                         congratulate_view,
                         surprise_view,
                         anniversary_view,
                         valentines_day_view,
                         festivals_view,
                         party_view,
                         special_with_cakes_view,
                         send_gifts_view,
                         propose_view)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^demon/', admin.site.urls),
    url(r'^$',home_view,name="home"),
    url(r'^cakes/',include('cakes.urls',namespace='cakes')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^about/us/',about_view,name="about"),
    url(r'^birthday/cakes/',birthday_view,name="birthday"),
    url(r'^marriage/cakes/',marriage_view,name="marriage"),
    url(r'^new-year/cakes/',new_year_view,name="new_year"),
    url(r'^congratulate/cakes/',congratulate_view,name="congratulate"),
    url(r'^surprise/cakes/',surprise_view,name="surprise"),
    url(r'^anniversary/cakes/',anniversary_view,name="anniversary"),
    url(r'^valentines/cakes/',valentines_day_view,name="valentines_day"),
    url(r'^festival/cakes/',festivals_view,name="festivals"),
    url(r'^party/cakes/',party_view,name="party"),
    url(r'^special/cakes/',special_with_cakes_view,name="special_with_cakes"),
    url(r'^gift/cakes/',send_gifts_view,name="send_gifts"),
    url(r'^propose/cakes/',propose_view,name="propose"),
]



