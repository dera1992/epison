import uuid
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from account.models import  Profile
from conference.models import Event


class AbstractManager(models.Manager):
    def active(self, *args, **kwargs):
        qs = self.get_queryset().filter(
            draft=False,
        )
        return qs

class Abstract(models.Model):

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True
    )
    event = models.ForeignKey(
        Event, blank=True, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=500)
    slug = models.SlugField(blank=True, max_length=500)
    name_author = models.CharField(max_length=500)
    corresponding_author = models.CharField(max_length=500)
    corresponding_author_phone = models.CharField(max_length=25)
    corresponding_author_email = models.EmailField(blank=True, null=True)
    background = RichTextUploadingField(blank=True, null=True)
    objective = RichTextUploadingField(blank=True, null=True)
    method = RichTextUploadingField(blank=True, null=True)
    result = RichTextUploadingField(blank=True, null=True)
    conclusion = RichTextUploadingField(blank=True, null=True)
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
    article_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False)
    approved_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="approved_by",
    )
    approved = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = AbstractManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = "-".join((slugify(self.title), slugify(self.created)))
        super(Abstract, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse("abstract:abstract-detail", args=[self.id])

    class Meta:
        verbose_name = _("Abstract")
        verbose_name_plural = _("Abstract")
        ordering = ["-created", "-updated"]





