from django.shortcuts import render,redirect
from mains.models import SlideImage
from cakes.models import Cake
from cakes.forms import CustomCakeForm
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def home_view(request):
	cakes = Cake.objects.order_by('-timestamp')
	cakes = cakes[:8]
	photos = SlideImage.objects.all()
	template = "index.html"
	cake_form = CustomCakeForm(request.POST or None,request.FILES or None)
	if cake_form.is_valid() and request.user.is_authenticated():
		custom = cake_form.save(commit=False)
		custom.user = request.user
		custom.save()
		messages.success("Your request has been successfully sent. We will get back to you soon")
		return redirect("/")

	context = {'photos':photos,
				'cakes':cakes,
				'cake_form':cake_form,}
	return render(request,template,context)

def about_view(request):
	template = "about.html"
	context = {}
	return render(request,template,context)
	
def birthday_view(request):
	cakes = Cake.objects.filter(cake_type='Birthday').order_by('-timestamp')
	paginator = Paginator(cakes, 8) 
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


	template = "birthday.html"
	cake_form = CustomCakeForm(request.POST or None,request.FILES or None)
	if cake_form.is_valid() and request.user.is_authenticated():
		custom = cake_form.save(commit=False)
		custom.user = request.user
		custom.save()
		messages.success("Your request has been successfully sent. We will get back to you soon")
		return redirect("/")

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)





