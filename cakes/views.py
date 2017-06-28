from django.shortcuts import render,redirect
from .models import Cake,OrderCake
from .forms import CakeOrderForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings 

# Create your views here.

def individual_view(request,slug):
	template = "individual.html"
	cake = Cake.objects.get(slug=slug)
	order_form = CakeOrderForm(request.POST or None)
	if order_form.is_valid() and request.user.is_authenticated():
		user = request.user
		email = request.user.email
		order = order_form.save(commit=False)

		phone_number = order_form.cleaned_data['phone_number']
		cake_message = order_form.cleaned_data['cake_message']
		delivery_date = order_form.cleaned_data['delivery_date']
		delivery_time = order_form.cleaned_data['delivery_time']
		quantity = order_form.cleaned_data['quantity']
		flavour = order_form.cleaned_data['flavour']
		weight = order_form.cleaned_data['weight']
		order.user = request.user 
		order.cake = cake
		order.save()
		# to get the price of given order
		objs = OrderCake.objects.order_by('-timestamp').first()
		price = str(objs.total_price())

		subject = 'Cake Order from ' + str(user)
		message = 'sender: %s \nFrom: %s \nCake Name: %s \nWeight: %s \nFlavour: %s \nPrice: %s \nPhone Number: %s \nDelivery Date: %s \nDelivery Time: %s \nQuantity: %s \n\nCake message: %s \n' %(user,email,cake,weight,flavour,price,phone_number,delivery_date,delivery_time,quantity,cake_message)
		
		emailFrom = email
		emailTo = [settings.EMAIL_HOST_USER]

		send_mail(subject,message,emailFrom,emailTo,fail_silently=True)
		messages.success(request,"Your order has been successfully submitted. We will get back to you soon via call or email.")
		return redirect("/")
	context = {'cake':cake,
				'order_form':order_form,}
	return render(request,template,context)

