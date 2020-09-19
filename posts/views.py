from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone 
from django.views.generic import View, ListView, DetailView, UpdateView

from .models import Post
from .forms import PostForm

from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy


class PostCreateUpdateView(UpdateView):
    model = Post
    template_name = "post_form.html"
    form_class = PostForm
    success_url = reverse_lazy("posts:list")

    def form_valid(self, form):
        if form.instance.slug:
            form.instance.updated_by = self.request.user
        else:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super(PostCreateUpdateView, self).get_initial()
        return initial

    def get_object(self, queryset=None):
        if self.kwargs.get("slug"):
            return super(PostCreateUpdateView, self).get_object()
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(PostDetailView, self).get_context_data(**kwargs)
        ctx['popular_posts'] = Post.objects.filter(view_count__gte=20)
        # import ipdb; ipdb.set_trace()
        return ctx


class PostListView(ListView):
    model = Post
    template_name = 'homepage.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        query=request.GET.get("q")
        if query:
            qs = qs.filter(
              Q(title__icontains=query) |
              Q(content__icontains=query) |
              Q(user__first_name__icontains=query)|
              Q(user__last_name__icontains=query)
            ).distinct()
        self.object_list = qs
        context = self.get_context_data(object_list=self.object_list)
        return render(request, self.template_name, context=context)
    
    def get_queryset(self):
        qs = Post.objects.filter(draft=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super(PostListView, self).get_context_data(**kwargs)
        ctx['popular_posts'] = self.get_queryset().filter(view_count__gte=20)
        return ctx

