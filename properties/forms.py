from django import forms
from .models import OrderProperty, InspectProperty


class PropertyRentForm(forms.ModelForm):
    start_date = forms.DateTimeField(label='Datetime', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    
    class Meta:
        model = OrderProperty
        fields = [
          'start_date',
          'message',
        ]


class PropertyInspectForm(forms.ModelForm):
    inspect_datetime = forms.DateTimeField(label='Datetime', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False)
    
    class Meta:
        model = InspectProperty
        fields = [
          'inspect_datetime',
          'message',
        ]
