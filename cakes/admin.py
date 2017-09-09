from django.contrib import admin
from .models import Cake,CustomCake,OrderCake

# Register your models here.

class CakeAdmin(admin.ModelAdmin):

	list_display = ['name','price','cake_type','flavour','weight']
	list_display_links = ['name']
	list_editable = []
	list_filter = ['timestamp']
	search_fields = ['name']
	class meta:
		model = Cake

admin.site.register(Cake,CakeAdmin)

admin.site.register(CustomCake)
admin.site.register(OrderCake)
