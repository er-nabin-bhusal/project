from django.shortcuts import render,redirect
from mains.models import SlideImage
from cakes.models import Cake,OrderCake
from cakes.forms import CustomCakeForm
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# for_ search
from django.db.models import Q

# send mail

from django.core.mail import send_mail
from django.conf import settings 

# Create your views here.

def home_view(request):
	title = "home"
	queryset_list = Cake.objects.order_by('-timestamp')

	query=request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(name__icontains=query) |
			Q(cake_type__icontains=query) |
			Q(description__icontains=query) |
			Q(price__icontains=query)
			).distinct()#it cant have duplicate elements now

	paginator = Paginator(queryset_list, 8) 
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

	photos = SlideImage.objects.all()
	template = "index.html"

	# adding to the cart
	orders = None
	if request.user.is_authenticated():
		orders = OrderCake.objects.filter(user=request.user)

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


	context = {'photos':photos,
				'home':title,
				'page_request_var':page_request_var,
				'cakes':queryset,
				'cake_form':cake_form,
				'orders':orders,}
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)


def marriage_view(request):
	cakes = Cake.objects.filter(cake_type='Marriage').order_by('-timestamp')
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


	template = "marriage.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)


def new_year_view(request):
	cakes = Cake.objects.filter(cake_type='New year').order_by('-timestamp')
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


	template = "new_year.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

def congratulate_view(request):
	cakes = Cake.objects.filter(cake_type='Congratulate').order_by('-timestamp')
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


	template = "congratulate.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

def surprise_view(request):
	cakes = Cake.objects.filter(cake_type='Surprise').order_by('-timestamp')
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


	template = "surprise.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

def anniversary_view(request):
	cakes = Cake.objects.filter(cake_type='Anniversary').order_by('-timestamp')
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


	template = "anniversary.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

def valentines_day_view(request):
	cakes = Cake.objects.filter(cake_type='Valentines Day').order_by('-timestamp')
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


	template = "valentinesday.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

def festivals_view(request):
	cakes = Cake.objects.filter(cake_type='Festivals').order_by('-timestamp')
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


	template = "festivals.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

def party_view(request):
	cakes = Cake.objects.filter(cake_type='Party').order_by('-timestamp')
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


	template = "party.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)

def special_with_cakes_view(request):
	cakes = Cake.objects.filter(cake_type='Special with Cakes').order_by('-timestamp')
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


	template = "special_with_cakes.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)



def send_gifts_view(request):
	cakes = Cake.objects.filter(cake_type='Send Gifts').order_by('-timestamp')
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


	template = "send_gifts.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)


def propose_view(request):
	cakes = Cake.objects.filter(cake_type='Propose').order_by('-timestamp')
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


	template = "propose_him_her.html"
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

	context = {'cakes':queryset,
				'page_request_var':page_request_var,
				'cake_form':cake_form,}
	return render(request,template,context)





