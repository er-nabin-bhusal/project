from django.shortcuts import render, redirect
from itertools import chain
from django.urls import reverse
from properties.models import Property, OrderProperty, RentProperty
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum
from django.views.generic import View, ListView

from django.core.mail import send_mail
from django.conf import settings 
from properties.utils import handle_discounts
from django.http import JsonResponse
from django.core.mail import send_mail
from project.settings import EMAIL_HOST_USER
from mains.models import Contact, SlideImage
from properties.models import OrderProperty, RentProperty

# Create your views here.

class HomeView(ListView):
    model = Property
    template_name = 'index.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        query=request.GET.get("q")
        if query:
            qs = qs.filter(
              Q(name__icontains=query) |
              Q(description__icontains=query) |
              Q(price__icontains=query)
            ).distinct()
        self.object_list = qs
        context = self.get_context_data(object_list=self.object_list)
        return render(request, self.template_name, context=context)
    
    def get_queryset(self):
        qs = Property.objects.filter(sold=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['photos'] = SlideImage.objects.all()
        if self.request.user.is_authenticated:
            orders = OrderProperty.objects.filter(user=self.request.user, paid=False).select_related('property', 'user')
            rents = RentProperty.objects.filter(user=self.request.user, paid=False).select_related('property', 'user')
            result_list = list(chain(orders, rents))
            total_price = 0
            for i in result_list:
              total_price += i.property.price
            ctx['orders'] = result_list
            ctx['total_price'] = total_price
        return ctx


def about_view(request):
	template = "about.html"
	context = {}
	return render(request,template,context)


def privacy_policy_view(request):
	template = "privacy_policy.html"
	context = {}
	return render(request,template,context)


class ContactView(View):

    def send_email(self, data, *args):
        send_mail(
            subject = data.get('subject'),
            message = data.get('message'),
            from_email = EMAIL_HOST_USER,
            recipient_list = [data.get('email')],
            fail_silently=False
        )

    def post(self, request, *args, **kwargs):
        data = request.POST
        c_obj = Contact(
          name=data['name'],
          email=data['email'],
          subject=data['subject'],
          message=data['message']
        )
        c_obj.save()
        self.send_email(data)
        messages.success(request, "Thank you for reaching out. We will get back to you soon.")
        return redirect(reverse('home'))


class PurchaseHistoryView(ListView):
    model = OrderProperty
    template_name = 'history.html'

    def get_queryset(self):
        qs = OrderProperty.objects.filter(paid=True).select_related('property')
        result_list = list(chain(qs, RentProperty.objects.filter(paid=True).select_related('property')))
        return result_list

    def get_context_data(self, **kwargs):
        ctx = super(PurchaseHistoryView, self).get_context_data(**kwargs)
        # ctx['rent_list'] = RentProperty.objects.filter(paid=True)
        return ctx