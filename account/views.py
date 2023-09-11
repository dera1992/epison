from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from .forms import ProfileForm, UserRegistrationForm, \
UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from account.tokens import account_activation_token
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import get_template
from account.models import Profile

from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        print(user_form )
        print(profile_form)
        if user_form.is_valid()and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = get_template('registration/account_activation_email.html').render({
                 'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message,from_email='Rockflint <rockflint20@gmail.com>', to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'An email has been sent to you,please go and activate your account')
            return redirect('home:home')
    else:
        user_form = UserRegistrationForm()
        profile_form =ProfileForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form,'profile_form': profile_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                        'account/edit.html',
                        {'user_form': user_form,
                        'profile_form': profile_form})

@login_required
def profile_display(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,
                        'account/edit_display.html',
                        {'profile': profile,})

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Your account has been confirm successfully')
        return redirect('home:home')
    else:
        messages.error(request, 'There is an error confirming your account')
        return render(request, 'registration/account_activation_invalid.html')

def membership_benefit(request):
    return render(request,
                        'account/membership.html',{})