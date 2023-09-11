from django.contrib import admin

from .models import Abstract



@admin.register(Abstract)
class AbstractAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "get_event",
        "approved",
        "created",
        "updated",
    ]
    list_filter = ["approved", "created", "updated"]
    list_editable = ["approved"]
    readonly_fields = ["article_id"]

    @admin.display(ordering='event__title', description='Event')
    def get_event(self, obj):
        return obj.event.title

    def save_model(self, request, obj, form, change):
        from django.core.mail import send_mail

        if request.user.is_superuser:
            if obj.approved:
                receiver = [obj.profile.user.email]
                to = receiver
                send_mail(
                    "Approved Abstract",
                    f"Congratulations your research {obj.title} has been approved successfully!",
                    "covidregister@ncrc.org.ng",
                    to,
                )
                super().save_model(request, obj, form, change)
            else:
                return super().save_model(request, obj, form, change)
        else:
            return super().save_model(request, obj, form, change)


