# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Abstract
from account.models import Profile
from .forms import AbstractEditForm, AbstractForm
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


User = get_user_model()

@login_required
def create_abstract(request):
    contact_email = "ezechdr16@gmail.com"
    # users = User.objects.filter(is_staff=True, is_superuser=True)
    admins = User.objects.filter(is_superuser=True).all()
    if admins:
        # receiver = list(i for i in users.values_list('email', flat=True) if bool(i))
        send_to = random.choice([user.email for user in admins])
        receiver = [send_to]
    else:
        receiver = [contact_email]

    if request.method == "POST":

        abstractForm = AbstractForm(request.POST, request.FILES)

        if abstractForm.is_valid():
            abstract_form = abstractForm.save(commit=False)
            abstract_form.profile = request.user.profile
            abstract_form.save()
            abstractForm.save_m2m()
            current_site = get_current_site(request)
            subject = "Approve Abstract"

            message = get_template("registration/abstract_approval_email.html").render(
                {
                    "user": request.user,
                    "domain": current_site.domain,
                    "id": abstract_form.id,
                    # "admin_url": settings.ADMIN_URL,
                }
            )
            to_email = receiver
            email = EmailMessage(
                subject,
                message,
                to=to_email,
                # to=[to_email],
            )
            email.content_subtype = "html"
            email.send()
            messages.success(
                request,
                "Your abstract has been created succcessfully. Please wait for approval",
            )

            return redirect("abstract:my-abstract")
        else:
            messages.error(request, "Sorry,Error creating your abstract")
    else:
        abstractForm = AbstractForm()

    return render(request, 'abstract/create.html',{"abstractForm": abstractForm})

@login_required
def edit_abstract(request, pk):
    abstract = Abstract.objects.get(id=pk)

    if abstract.profile.user != request.user:
        raise Http404()

    if request.method == "POST":

        abstractForm = AbstractEditForm(request.POST, request.FILES)

        if abstractForm.is_valid():
            abstract_form = abstractForm.save(commit=False)
            abstract_form.profile = request.user.profile
            abstract_form.current = True
            abstract_form.save()
            abstractForm.save_m2m()

            messages.success(
                request, "{} has been successfully updated!".format(abstract.study_title)
            )
            return redirect("abstract:my-abstract")

        else:
            messages.error(request, "Sorry,Error updating your research")
    else:
        abstractForm = AbstractEditForm(instance=abstract)
    return render(request, 'abstract/edit.html',{"abstractForm": abstractForm})

def detail_abstract(request, pk):
    abstract = get_object_or_404(Abstract, id=pk)
    abstract_similar = (
        Abstract.objects.filter(event=abstract.event, approved=True)
            .exclude(id=abstract.id)
            .order_by("?")[:3]
    )

    return render(request, 'abstract/detail.html', {
            "abstract": abstract,
            "abstract_similar": abstract_similar,
        },)

@login_required
def delete_abstract(request, pk=None):
    ad = Abstract.objects.get(id=pk)
    if (
        request.user != ad.profile.user
        or not request.user.is_staff
        or not request.user.is_superuser
    ):
        raise Http404()
    ad.approved = False
    messages.success(request, "Successfuly deleted")
    return redirect("abstract:my-abstract")

def list_abstract(request):
    abstracts_list = Abstract.objects.filter(approved=True).order_by("-created")
    paginator = Paginator(abstracts_list, 8)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return render(request, 'abstract/list.html',{"abstracts": queryset})

@login_required
def my_abstract(request):
    myab_list = Abstract.objects.filter(profile__user=request.user).order_by("-created", "?")
    paginator = Paginator(myab_list, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    profile = Profile.objects.get(user=request.user)

    return render(request, 'abstract/my_abstract.html',{
            "myab": queryset,
            "profile": profile,
        },)