from django.db import models
from django.conf import settings

class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    membership_type = models.ForeignKey(Type,
                                 on_delete=models.CASCADE,null=True,blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255,null=True,blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)
    google = models.URLField(max_length=255, null=True, blank=True)
    linkedin = models.URLField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='profile/%Y/%m/%d/',blank=True, default='profile/None/avater.png')
    email_confirmed = models.BooleanField(default=False)
    active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.first_name

    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)

