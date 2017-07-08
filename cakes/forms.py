from django import forms
from .models import CustomCake,OrderCake



class CustomCakeForm(forms.ModelForm):
	name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
	contact = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
	phone = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Phone Number'}))
	details = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Enter Details.'}))
	class Meta:
		model = CustomCake
		fields = [
			'name',
			'contact',
			'phone',
			'details',
			'image',
		]

class CakeOrderForm(forms.ModelForm):
	delivery_date = forms.DateField(widget=forms.SelectDateWidget)
	delivery_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time','placeholder':'HH:MM:SS enter in 24 hour format.'}))
	cake_message = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = OrderCake
		fields = [
		'weight',
		'flavour',
		'quantity',
		'eggless',
		'delivery_date',
		'delivery_time',
		'phone_number',
		'cake_message',
		]