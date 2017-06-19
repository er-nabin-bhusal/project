from django.contrib import admin
from .models import Cake,CustomCake,OrderCake

# Register your models here.
admin.site.register(Cake)
admin.site.register(CustomCake)
admin.site.register(OrderCake)
