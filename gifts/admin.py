from django.contrib import admin
from .models import Pillo,OrderPillo 
from django.db.models.functions import Lower
# Register your models here.
class PilloAdmin(admin.ModelAdmin):

	list_display = ['name','price','pk']
	list_display_links = ['name']
	list_editable = ['price']
	list_filter = ['timestamp']
	search_fields = ['name','pk']
	ordering = ['name']
	def get_ordering(self, request):
		return [Lower('name')]
	class meta:
		model = Pillo

admin.site.register(Pillo,PilloAdmin)
admin.site.register(OrderPillo)
