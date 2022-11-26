from django.contrib import admin
from .models import UserProfile, Device, IPModel, Pending, Credential

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created",
    )
    ordering = ("-created",)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Device)
admin.site.register(IPModel)
admin.site.register(Pending)
admin.site.register(Credential)