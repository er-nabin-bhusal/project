from django.shortcuts import render, redirect, reverse
from .models import Property, OrderProperty, InspectProperty, RentProperty
from .forms import PropertyInspectForm, PropertyRentForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 
from django.views.generic import ListView, View, DetailView

# Create your views here.

class PropertyView(DetailView):
    model = Property
    template_name = 'individual.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        ctx = super(PropertyView, self).get_context_data(**kwargs)
        ctx['rent_form'] = PropertyRentForm(self.request.GET or None)
        ctx['inspect_form'] = PropertyInspectForm(self.request.GET or None)
        obj = self.get_object()
        if self.request.user.is_authenticated:
            ctx['is_under_inspect'] = True if InspectProperty.objects.filter(user=self.request.user, property=obj).count() > 0 else False
        return ctx


class BuyPropertyListView(ListView):
    model = Property
    template_name = 'buy-property.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Property.objects.filter(type='sell', sold=False)
        return qs


class RentPropertyListView(ListView):
    model = Property
    template_name = 'rent-property.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Property.objects.filter(type='rent', sold=False)
        return qs


class PostInspectionView(View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        obj = InspectProperty(
          user=request.user,
          property_id=self.kwargs.get('pk'),
          inspect_datetime=data.get('inspect_datetime'),
          message=data.get('message'),
        )
        obj.save()
        messages.success(request, "You have successfully ordered an inspection. We will get back to you soon.")
        return redirect(reverse('home'))


class BuyPropertyView(View):
    def get(self, request, *args, **kwargs):
        property = Property.objects.get(id=self.kwargs.get('pk'))
        if OrderProperty.objects.filter(user=request.user, property=property, paid=False):
            messages.warning(request, "You have already placed an order for this property. Consider checkout.")
            return redirect(reverse('home'))
        obj = OrderProperty(
          user=request.user,
          property=property,
          message='Property Bought',
        )
        obj.save()
        messages.success(request, "You have successfully ordered a product. Please proceed to checkout")
        return redirect(reverse('home'))


class RentPropertyView(View):
    def post(self, request, *args, **kwargs):
        property = Property.objects.get(id=self.kwargs.get('pk'))
        data = request.POST
        if RentProperty.objects.filter(user=request.user, property=property, paid=False):
            messages.warning(request, "You have already placed an order for this property. Consider checkout.")
            return redirect(reverse('home'))
        obj = RentProperty(
          user=request.user,
          property=property,
          start_date=data.get('start_date'),
          message=data.get('message')
        )
        obj.save()
        messages.success(request, "You have successfully rented a product. Please proceed to checkout")
        return redirect(reverse('home'))


class CheckoutPurchaseView(View):
    def get(self, request, *args, **kwargs):
        rent_objs = RentProperty.objects.filter(user=request.user)
        buy_objs = OrderProperty.objects.filter(user=request.user)
        for rent in rent_objs:
            rent.paid = True
            property = rent.property
            property.sold = True
            property.save()
            rent.save()
        for buy in buy_objs:
            buy.paid = True
            property = buy.property
            property.sold = True
            property.save()
            buy.save()
        messages.success(request, "You have successfully purchased a product.")
        return redirect(reverse('home'))


class RemoveFromPurchaseList(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        type = self.kwargs.get('type')
        if type == 'rent':
            RentProperty.objects.filter(pk=pk).delete()
        else:
            OrderProperty.objects.filter(pk=pk).delete()
        messages.success(request, "You removed a product from your booking list. Please continue shopping.")
        return redirect(reverse('home'))
