from django import forms
from .models import Pillo,OrderPillo

class PilloOrderForm(forms.ModelForm):
	delivery_date = forms.DateField(widget=forms.SelectDateWidget)
	delivery_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time','placeholder':'HH:MM:SS enter in 24 hour format.'}))
	gift_message = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = OrderPillo
		fields = [
		'quantity',	
		'delivery_date',
		'delivery_time',
		'phone_number',
		'gift_message',
		]