from django.urls import path
from posts import views

app_name = "posts"

urlpatterns = [
	path('list', views.PostListView.as_view(), name="list"),
 	path('create/', views.PostCreateUpdateView.as_view(), name='create'),
 	path('<str:slug>/', views.PostDetailView.as_view(), name='detail'),
 	path('<str:slug>/edit/', views.PostCreateUpdateView.as_view(), name='update'),
 	# path('<slug>/delete/', views.post_delete),
]
