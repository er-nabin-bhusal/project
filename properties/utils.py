from django.contrib.auth import get_user_model
# importing user mode to User
User = get_user_model() 

from properties.models import OrderProperty

def handle_discounts(user,*args,**kwargs):
    logged_in_user = user
    total_orders = OrderProperty.objects.filter(user=logged_in_user)
    if total_orders.count() != 0:
      if total_orders.count() == 1:
        value = "Congratulations, You will get a discount on your next order of"
        percentage = 10
      elif total_orders.count() == 2:
        value = "Congratulations, You will get a discount on your next order of"
        percentage = 10
      else:
        value = "Congratulations, You will get a discount on every order of"
        percentage = 15
    else:
      value = "Thank you for  signing up. You will get a discount on you first order of "
      percentage = 5

    dic = {'offer':value, 'discount':percentage}
    return dic
