
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone 

from .models import Post
from .forms import PostForm

from django.db.models import Q


# for the commments we do this 
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser: 
		raise Http404
	
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.approval = True
		instance.save()
		messages.success(request,"Your Post has been created successfully. It will be posted within hours.")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'form':form,
	}
	return render(request,'post_form1.html',context)

def post_detail(request,slug=None):
	# instance = Post.objects.get(id=3)
	instance = get_object_or_404(Post, slug=slug)

	# raises view count
	instance.raise_view_count
	instance.save()

	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_superuser or not request.user.is_staff:
			raise Http404
	comments = Comment.objects.filter_by_instance(instance)


	# comment design here
	initial_data = {
	'content_type':instance.get_content_type,
	'object_id':instance.id,
	}

	form = CommentForm(request.POST or None,initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		# print(form.cleaned_data)
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count()==1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(

												user=request.user,
												content_type=content_type,
												object_id=obj_id,
												content=content_data,
												parent = parent_obj,

															)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	# most popular posts
	most_popular_posts = Post.objects.order_by('-view_count')[:4:] # it stores only the most visited 4 posts

	# your posts only
	your_posts = None;
	if  request.user.is_authenticated:
		your_posts = Post.objects.filter(user=request.user)


	context = {
	'most_popular_posts':most_popular_posts,
	'your_posts':your_posts,
	'comment_form':form,
	'comments':comments,
	'instance':instance,
	}
	return render(request,'post_detail.html',context)

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.all()
	if not request.user.is_staff or not request.user.is_superuser:
		queryset_list = Post.objects.active()
	
	query=request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()#it cant have duplicate elements now



	paginator = Paginator(queryset_list, 4) # Show 6 contacts per page
	page_request_var = "goto"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	
		queryset = paginator.page(1)
	except EmptyPage:
	
		queryset = paginator.page(paginator.num_pages)


	# most popular posts
	most_popular_posts = Post.objects.order_by('-view_count')[:4:] # it stores only the most visited 4 posts

	# your posts only
	your_posts = None;
	if  request.user.is_authenticated:
		your_posts = Post.objects.filter(user=request.user)

	context = {
	'your_posts':your_posts,
	'most_popular_posts':most_popular_posts,
	'page_request_var':page_request_var,
	'object_list': queryset,
	'today':today
	}


	return render(request,'homepage.html',context)


def post_update(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser: 
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.approval = True
		instance.save()
		messages.success(request,"<a href='#'>Item</a> successfully edited", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
	'form':form,
	'instance':instance,
	}
	return render(request,'post_form1.html',context)

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser: 
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request,"successfully deleted", extra_tags='html_safe')
	return redirect('posts:list')



	
