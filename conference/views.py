# Create your views here.
from __future__ import unicode_literals

import random
import string

from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from xhtml2pdf import pisa
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from account.models import Profile
from django.shortcuts import get_object_or_404, redirect, render
from .models import Event, Speaker, TimeBreakdown, EventImage, RegisterEvent
from .forms import RegForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

import io

def create_doi():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

@login_required
def certificate_view(request,pk):
    event = Event.objects.get(id=pk)
    profile = Profile.objects.get(user=request.user)
    # get the template for the certificate
    template = get_template('conference/certificate_template.html')

    # define the context to fill in the template
    context = {
        'certificate_title': 'Certificate of Attendance',
        'recipient_name': profile.fullname,
        'achievement': event.title,
        'date_of_issue': event.end_date,
    }

    # render the template with the context
    html = template.render(context)

    # create the PDF file
    pdf = pisa.CreatePDF(html)

    # if the PDF was created successfully, show the certificate as a web page with a download button
    if not pdf.err:
        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = 'inline; filename="certificate.html"'
        return response

    # if there was an error creating the PDF, return an error message
    return HttpResponse('Error generating PDF file', status=500)

@login_required
def download_certificate(request,pk):
    event = Event.objects.get(id=pk)
    profile = Profile.objects.get(user=request.user)
    # retrieve the relevant data for the certificate from the database or context

    # render the HTML template with the relevant data
    template = get_template('conference/certificate_template.html')
    context = {
        'certificate_title': 'Certificate of Attendance',
        'recipient_name': profile.fullname,
        'achievement': event.title,
        'date_of_issue': event.end_date,
    }
    html = template.render(context)

    # create a PDF file from the HTML template with CSS applied
    pdf_file = io.BytesIO()

    # define the desired width and height of the certificate
    certificate_width = '790px'
    certificate_height = '600px'

    # define custom page size and margins
    page_size = f'{certificate_width} {certificate_height}'
    page_margin = '0 20px 20px 0'  # top right bottom left

    # define custom CSS for page size and margins
    css = CSS(string=f'@page {{ size: {page_size}; margin: {page_margin}; }}')

    # create the PDF using WeasyPrint
    HTML(string=html).write_pdf(pdf_file, stylesheets=[css], font_config=FontConfiguration())

    # rewind the file pointer of the PDF file
    pdf_file.seek(0)

    # set the appropriate response headers for PDF download
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    return response


def detail_event(request, id, slug):
    event = get_object_or_404(Event, id=id,slug=slug)
    speakers = Speaker.objects.filter(events=event)
    time_breakdown = TimeBreakdown.objects.filter(events=event)
    return render(request, 'conference/detail.html',
                  {"event": event,
                   "speakers":speakers,
                   "time_breakdown": time_breakdown},)

def list_event(request):
    events_list = Event.objects.all().order_by('-created', '?')[:6]
    paginator = Paginator(events_list, 8)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return render(request, 'conference/list.html',
                  {"events": queryset},)

def detail_speaker(request, pk):
    speaker = get_object_or_404(Speaker, id=pk)
    return render(request, 'conference/speaker_detail.html',
                  {"speaker": speaker},)

@login_required
def register_event(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == "POST":
        regForm = RegForm(request.POST, request.FILES)

        if regForm.is_valid():
            reg_form = regForm.save(commit=False)
            reg_form.profile = request.user.profile
            reg_form.payment_id = create_doi()
            reg_form.event_registered = event  # Set the event_registered field
            reg_form.save()
            messages.success(
                request,
                "You have registered for this event. Please wait for approval",
            )
            return redirect("conference:my-event")
        else:
            messages.error(request, "Sorry, error registering for this event")
    else:
        regForm = RegForm()

    return render(request, 'conference/register.html', {"regForm": regForm, "event":event})


def gallery_event(request):
    events = Event.objects.all()
    photos = EventImage.objects.all()

    print(photos)

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            event = Event.objects.get(id=data['category'])
        else:
            event = None

        for image in images:
            photo = EventImage.objects.create(
                event_image=event,
                images=image,
            )
        messages.success(
            request,
            "Your images has been uploaded successfully"
        )
        return redirect('conference:event-gallery')

    context = {"events": events, 'photos':photos}
    return render(request, 'conference/gallery.html',context)

def viewPhoto(request, pk):
    photo = EventImage.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

@login_required
def my_registered_event(request):
    my_event = RegisterEvent.objects.filter(profile__user=request.user).order_by('-created')

    paginator = Paginator(my_event , 3)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get('page')
    try:
        my_ev = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        my_ev = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        my_ev = paginator.page(paginator.num_pages)
    return render(request, 'conference/my_registered_event.html',{'my_ev': my_ev,})