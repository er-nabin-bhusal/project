from django.urls import path
from properties.views import RemoveFromPurchaseList, CheckoutPurchaseView, RentPropertyView, BuyPropertyListView, RentPropertyListView, PostInspectionView, PropertyView, BuyPropertyView


app_name = "properties"


urlpatterns=[
  path("remove/<int:pk>/<str:type>/", RemoveFromPurchaseList.as_view(), name='remove_property'),
  path("detail/<str:slug>/", PropertyView.as_view(), name='individual_property'),
  path("buy-list/", BuyPropertyListView.as_view(), name='buy_property_list'),
  path("rent-list/", RentPropertyListView.as_view(), name='rent_property_list'),
  path("inspection/<int:pk>/", PostInspectionView.as_view(), name='property_inspection'),
  path("buy/<int:pk>/", BuyPropertyView.as_view(), name='property_buy'),
  path("rent/<int:pk>/", RentPropertyView.as_view(), name='property_rent'),
  path("checkout/", CheckoutPurchaseView.as_view(), name='checkout_purchase'),
]
