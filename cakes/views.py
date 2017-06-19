from django.shortcuts import render,redirect
from .models import Cake
from .forms import CakeOrderForm
from django.contrib import messages

# Create your views here.

def individual_view(request,pk):
	template = "individual.html"
	cake = Cake.objects.get(pk=pk)
	order_form = CakeOrderForm(request.POST or None)
	if order_form.is_valid() and request.user.is_authenticated():
		order = order_form.save(commit=False)
		order.user = request.user 
		order.cake = cake
		order.save()
		messages.success(request,"Your order has been successfully submitted. We will get back to you soon via call or email. To manage the order check your Cart.")
		return redirect("/")
	context = {'cake':cake,
				'order_form':order_form,}
	return render(request,template,context)

