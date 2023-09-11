from django.contrib import admin
from .models import Profile, Type

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','first_name','last_name' ,'phone', 'photo']


admin.site.register(Type)
