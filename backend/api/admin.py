from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Appointment, AdministratorAction, Note

# Register Profile Inline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fields = ['role', 'full_name', 'contact_number', 'address']

# Define a custom UserAdmin to include Profile inline
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['is_active']

    def role(self, obj):
        return obj.profile.role if hasattr(obj, 'profile') else None

    role.short_description = 'Role'

    def save_model(self, request, obj, form, change):
        # Save the user first
        obj.save()


# Unregister the default User admin and register the new UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Note)

# Check if Appointment model is registered
if Appointment in admin.site._registry:
    admin.site.unregister(Appointment)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['relief_recipient', 'consultant', 'date_time', 'status']
    list_filter = ['status', 'date_time']
    search_fields = ['relief_recipient__username', 'consultant__username']

class AdministratorActionAdmin(admin.ModelAdmin):
    list_display = ['administrator', 'user_affected', 'action_taken', 'action_date']
    list_filter = ['action_date']

# Register Appointment model and AdministratorAction model
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(AdministratorAction, AdministratorActionAdmin)
