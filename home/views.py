# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from conference.models import Event
from blog.models import Post, Category
from account.models import Profile
from conference.models import Speaker
from django.contrib.auth.decorators import login_required


def home(request):
    try:
        event = Event.objects.get(active=True)
    except Event.DoesNotExist:
        event = None

    blog = Post.objects.all().order_by('-created', '?')[:3]
    profile = Profile.objects.all()[:3]
    speakers = Speaker.objects.filter(events=event)

    return render(request, 'home/index.html', {
        'event': event, 'blog': blog, 'profile': profile, 'speakers': speakers
    })



@login_required
def dashboard(request):
    ads = Post.objects.all()
    return render(request,'home/dashboard.html', {})

