from django.shortcuts import render,redirect
from .models import Pillo,OrderPillo
from .forms import PilloOrderForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 

from mains.models import SlideImage
from cakes.forms import CustomCakeForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# for_ search
from django.db.models import Q

# send mail

from cakes.utils import handle_discounts

# Create your views here.

def individual_view(request,slug):
	template = "individual_gift.html"
	gift = Pillo.objects.get(slug=slug)
	s = gift.raise_view_count()
	gift.save()

	order_form = PilloOrderForm(request.POST or None)
	if order_form.is_valid() and request.user.is_authenticated():
		user = request.user
		email = request.user.email
		order = order_form.save(commit=False)

		phone_number = order_form.cleaned_data['phone_number']
		gift_message = order_form.cleaned_data['gift_message']
		delivery_date = order_form.cleaned_data['delivery_date']
		delivery_time = order_form.cleaned_data['delivery_time']
		quantity = order_form.cleaned_data['quantity']
		order.user = request.user 
		order.gift = gift
		order.save()
		# to get the price of given order
		objs = OrderPillo.objects.order_by('-timestamp').first()
		price = str(objs.total_price())

		subject = 'Gift Order from ' + str(user)
		message = 'Product Id: %s \nsender: %s \nFrom: %s \nGift Name: %s \nPrice: %s \nPhone Number: %s \nDelivery Date: %s \nDelivery Time: %s \nQuantity: %s \n\nGift message: %s \n' %(gift.pk,user,email,gift,price,phone_number,delivery_date,delivery_time,quantity,gift_message)
		
		emailFrom = email
		emailTo = [settings.EMAIL_HOST_USER]

		send_mail(subject,message,emailFrom,emailTo,fail_silently=True)
		messages.success(request,"Your order has been successfully submitted. We will get back to you soon via call or email.")
		return redirect("/")
	context = {'gift':gift,
				'order_form':order_form,}
	return render(request,template,context)


def gift_view(request):
	gifts = Pillo.objects.all()
	paginator = Paginator(gifts, 8) 
	page_request_var = "goto"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	template = "gifts.html"

	cake_form = CustomCakeForm(request.POST or None,request.FILES or None)
	if cake_form.is_valid() and request.user.is_authenticated():

		phone = cake_form.cleaned_data['phone']
		details = cake_form.cleaned_data['details']
		name = cake_form.cleaned_data['name']
		email = cake_form.cleaned_data['contact']

		subject = 'Custom Cake Order from ' + str(request.user)
		message = 'sender: %s \nFrom: %s\nName: %s\nPhone Number: %s\n\nCake message: %s \n' %(request.user,email,name,phone,details)
		emailFrom = email
		emailTo = [settings.EMAIL_HOST_USER]

		send_mail(subject,message,emailFrom,emailTo,fail_silently=True)
		custom = cake_form.save(commit=False)
		custom.user = request.user
		custom.save()
		messages.success(request,"Your request has been successfully sent. We will get back to you soon")
		return redirect("/")

	context = {'gifts':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

