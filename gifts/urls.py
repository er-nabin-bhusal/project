from django.conf.urls import url
from gifts.views import individual_view,gift_view



urlpatterns=[

url(r'^pillow/',gift_view,name="send_gifts"),
url(r'^(?P<slug>[\w-]+)/$', individual_view, name='individual_gift'),

]