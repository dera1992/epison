from django.contrib import admin

from .models import TimeBreakdown, State,\
    Event, Speaker, EventImage, RegisterEvent

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'lat','long']

class TimeBreakdownInline(admin.StackedInline):
    model = TimeBreakdown

class SpeakerInline(admin.StackedInline):
    model = Speaker


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date','end_date','created']
    list_filter = ['created', 'address']
    search_fields = ['title', 'address']
    inlines = [SpeakerInline, TimeBreakdownInline]

    def save_model(self, request, obj, form, change):

        if request.user.is_superuser:
            if obj.active:
                Event.objects.filter(active=True).update(
                    active=False
                )
                super().save_model(request, obj, form, change)
            else:
                return super().save_model(request, obj, form, change)
        else:
            return super().save_model(request, obj, form, change)

@admin.register(RegisterEvent)
class RegisterEventAdmin(admin.ModelAdmin):
    list_display = ['payment_id','get_event','get_payee','approved_payment','prove_of_payment','created']
    list_filter = ['payment_id', 'created']
    search_fields = ['payment_id', 'get_event']

    @admin.display(ordering='event_registered__title', description='Event')
    def get_event(self, obj):
        return obj.event_registered.title

    @admin.display(ordering='profile__first_name', description='User')
    def get_payee(self, obj):
        return obj.profile.fullname

admin.site.register(EventImage)