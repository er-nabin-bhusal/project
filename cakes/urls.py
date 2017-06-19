from django.conf.urls import url
from cakes.views import individual_view



urlpatterns=[

url(r'^(?P<pk>\d+)$', individual_view, name='individual_cake'),

]