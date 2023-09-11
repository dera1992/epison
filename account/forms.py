from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile,Type

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='',
         widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ))
    password2 = forms.CharField(label='',
         widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}
        ))
    username = forms.CharField(label='',help_text=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        ))
    email = forms.EmailField(label='',
       widget=forms.EmailInput(
           attrs={'class': 'form-control', 'placeholder': 'Email'}
       ))

    class Meta:
        model = User
        fields = ('username','email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already used")

        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used")

        return email

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name','label':''}
        ),label='',
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name',}
        ),label='',
    )
    membership_type = forms.ModelChoiceField(
        queryset=Type.objects.all(), to_field_name='id', required=True,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'membership type'}
        ),label='',initial=1)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'membership_type')



class UserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = ('username','email')
        help_texts = {
            'username': None,
        }


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}
        )
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'eg: +234 8030793112'}
        )
    )
    membership_type = forms.ModelChoiceField(
        queryset=Type.objects.all(), to_field_name='id', required=True,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'membership type'}
        ), label='',
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Address'}
        ), required=False
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20, 'class': 'form-control',})
                                  ,label='About', required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','phone', 'address', 'photo','membership_type',
                  'facebook','twitter','google','linkedin','description')

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'filestyle'})