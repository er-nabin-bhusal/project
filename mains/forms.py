from django import forms
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=225)
    last_name = forms.CharField(max_length=225)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user