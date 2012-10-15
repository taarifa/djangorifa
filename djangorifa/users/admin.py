from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import transaction

from registration.models import RegistrationProfile

admin.site.unregister(User)
admin.site.unregister(RegistrationProfile)

class TaarifaUserAdmin(UserAdmin):
    actions = ['activate_users', 'resend_activation_email']

    def __init__(self, *args, **kwargs):
        super(TaarifaUserAdmin, self).__init__(*args, **kwargs)
        self.list_display = self.list_display + ('is_active', 'activation_key_expired')
        self.list_editable = self.list_editable + ('is_active',)
        self.raw_id_fields = ['user']
        search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def activation_key_expired(self, obj):
        return RegistrationProfile.objects.get(user=obj).activation_key_expired()
    activation_key_expired.boolean = True

    """
    Activates the selected users, if they are not alrady
    activated.

    """
    @transaction.commit_on_success
    def activate_users(self, request, queryset):
        for user in queryset:
            profile = RegistrationProfile.objects.get(user=user)
            RegistrationProfile.objects.activate_user(profile.activation_key)
    activate_users.short_description = ("Activate users")

    """
    Re-sends activation emails for the selected users.

    Note that this will *only* send activation emails for users
    who are eligible to activate; emails will not be sent to users
    whose activation keys have expired or who have already
    activated.

    """
    @transaction.commit_on_success
    def resend_activation_email(self, request, queryset):
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        for user in queryset:
            profile = RegistrationProfile.objects.get(user=user)
            if not profile.activation_key_expired():
                profile.send_activation_email(site)
    resend_activation_email.short_description = ("Re-send activation emails")


admin.site.register(User, TaarifaUserAdmin)
