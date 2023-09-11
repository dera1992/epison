# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from account.models import Profile
from .forms import InformationForm
from django.core.mail import EmailMessage


def create_contact(request):
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            post_info = form.save(commit=False)

            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Compose the email
            email_subject = f'Contact Form Submission: {subject}'
            email_message = f'Hello "{name}" sent you a message below:\n\n{message}'

            # Set the sender and recipient
            from_email = email
            to_email = 'ezechdr16@gmail.com'

            # Create and send the email
            email = EmailMessage(
                email_subject, email_message, from_email, [to_email]
            )
            email.send()

            # Save the form data
            post_info.save()

            messages.success(request, 'Your message has been received.')
            return redirect('info:contact')
        else:
            return redirect('info:contact')

    else:
        form = InformationForm()

    return render(request, 'info/contact.html', {'form': form})


def about_us(request):
    profile = Profile.objects.all()[:3]
    return render(request, 'info/about.html',{'profile': profile})


