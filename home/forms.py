from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django import forms


class MessageForm(forms.Form):
    phone = forms.CharField(max_length=25,required=True,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Phone', }
                           ), label='',
                           )
    email = forms.EmailField(
        label='',required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        )
    )
    comments = forms.CharField(required=True,
                               widget=forms.Textarea(
                               attrs={'class': 'form-control', 'placeholder': 'Message', }
                           ), label='',)


class ScheduleForm(forms.Form):
    date = forms.DateField(required=True,
                           widget=DatePickerInput(format='%m/%d/%Y',attrs={'placeholder': 'Date'}), label='',
                           )
    time = forms.TimeField( required=True,
                            widget=TimePickerInput(attrs={'placeholder': 'Time', }),label='',
                            )
    name = forms.CharField(max_length=255, required=True,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Name', }
                            ), label='',
                            )
    phone = forms.CharField(max_length=25, required=True,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Phone', }
                            ), label='',
                            )

    message = forms.CharField(required=True,
                               widget=forms.Textarea(
                               attrs={'class': 'form-control', 'placeholder': 'Message', }
                           ), label='',)



