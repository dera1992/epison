from django import forms
from django.forms import ModelForm
from .models import RegisterEvent, Event

class RegForm(ModelForm):

    event_registered = forms.ModelChoiceField(
        queryset=Event.objects.all(), to_field_name='id', required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': '', 'type': 'hidden'}
        ), label='',)
    payment_id = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '','type': 'hidden' }
        ), label='', required=False,
    )

    class Meta:
        model = RegisterEvent
        fields = ('prove_of_payment','event_registered','payment_id')

    # def __init__(self, *args, event_choices=None, **kwargs):
    #     super(RegForm, self).__init__(*args, **kwargs)
    #     self.fields['prove_of_payment'].widget.attrs.update({'class': 'filestyle'})
    #     if event_choices:
    #         self.fields['event_registered'].choices = event_choices