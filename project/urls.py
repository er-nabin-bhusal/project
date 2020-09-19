from django.urls import include, path
from django.contrib import admin
from mains.views import HomeView, about_view, privacy_policy_view, ContactView, PurchaseHistoryView

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "FOUR SQUARE RENTAL"
admin.site.site_title = "FOUR SQUARE RENTAL Admin Portal"
admin.site.index_title = "Welcome to FOUR SQUARE RENTAL Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("contact/", ContactView.as_view(), name="contact"),
    path("agents/", include("agents.urls", namespace="agents")),
    path("", HomeView.as_view(), name="home"),
    path("property/",include('properties.urls',namespace='properties')),
    path("purchase-history/", PurchaseHistoryView.as_view(), name="purchase_history"),
    path("accounts/", include('allauth.urls')),
    path("about/", about_view,name="about"),
    path("privacy_policy/", privacy_policy_view,name="privacy_policy"),
    path("blog/", include('posts.urls', namespace="posts")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



