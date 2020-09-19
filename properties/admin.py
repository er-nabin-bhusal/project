from django.contrib import admin
from .models import Property, OrderProperty, InspectProperty, RentProperty
from django.db.models.functions import Lower


class PropertyAdmin(admin.ModelAdmin):

    list_display = ['name', 'price', 'type', 'sold']
    list_display_links = ['name']
    list_filter = ['type']
    search_fields = ['name', 'pk']
    ordering = ['name']

    def get_ordering(self, request):
        return [Lower('name')]

    class meta:
        model = Property


admin.site.register(Property, PropertyAdmin)
admin.site.register(OrderProperty)
admin.site.register(InspectProperty)
admin.site.register(RentProperty)
