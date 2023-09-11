# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.contrib.auth.models import User
from django.db import models
from account.models import Profile
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField




class State(models.Model):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)
    long = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("State")


class EventQuerySet(models.query.QuerySet): #for active
    def active(self):
        return self.filter(active=True)

class EventManager(models.Manager):#for active
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()
# Create your models here.


class Event(models.Model):

    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE)
    title =models.CharField( max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255,blank=True)
    description = RichTextUploadingField(blank=True, null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    registration_deadline = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    thumbnail = models.ImageField(upload_to='event/',
                                   null=True, blank=True,default='profile/None/no_image.png')
    event_id = models.UUIDField(default=uuid.uuid4, unique=True,
                                  editable=False)
    follow_up = models.CharField(max_length=25, null=True, blank=True)
    bank = models.CharField(max_length=25, null=True, blank=True)
    account_no = models.CharField(max_length=25, null=True, blank=True)
    account_name = models.CharField(max_length=200, null=True, blank=True)

    active = models.BooleanField(default=True)
    objects = EventManager()#for active

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('conference:event-detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-end_date']

    @property
    def event_status(self):
        status = None

        present = datetime.now().timestamp()
        deadline = self.registration_deadline.timestamp()
        past_deadline = (present > deadline)

        if past_deadline:
            status = 'Finished'
        else:
            status = 'Ongoing'

        return status

class TimeBreakdown(models.Model):
    description = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)
    events = models.ForeignKey(Event, related_name="timebreakdown", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.events.title

    class Meta:
        verbose_name = _("TimeBreakdown")
        verbose_name_plural = _("TimeBreakdown")

class Speaker(models.Model):
    events = models.ForeignKey(Event, related_name="speakers", on_delete=models.CASCADE, default=0)
    speaker_image = models.ImageField(upload_to='images/', default='profile/None/no_image.png', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank = True)
    twitter = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    facebook = models.URLField(max_length=500, null=True, blank=True)

    def get_ordering_queryset(self):
        return self.events.speakers.all()

    def get_absolute_url(self):
        return reverse('conference:speaker-detail', args=[self.id])

    class Meta:
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speaker")


class EventImage(models.Model):
    event_image = models.ForeignKey(Event, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="img", default='profile/None/no_image.png', null=True, blank=True)

    def __str__(self):
        return self.event_image.title

class RegisterEvent(models.Model):
    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE)
    event_registered = models.ForeignKey(Event, on_delete=models.CASCADE)
    prove_of_payment = models.ImageField(upload_to="img", default='profile/None/no_image.png', null=True, blank=True)
    approved_payment = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=25, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.event_registered.title

    def get_absolute_url(self):
        return reverse('conference:download_certificate', args=[self.event_registered.id])