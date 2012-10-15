from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from taarifa_config.models import TaarifaConfig
from users.models import UserProfile

class CheckConfigSet(object):
    def process_request(self, request):
        count = TaarifaConfig.objects.count()
        redirect_url = reverse('taarifa_config:setup')
        login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
        logout_url = '/accounts/logout/'
        if not request.path in [redirect_url, login_url, logout_url] and not count and request.user.has_perm('taarifa_config.add_taarifaconfig'):
            # Clearly the user profile has not been created at this point, so need to create one
            UserProfile.objects.get_or_create(user=request.user)

            # Additionally need to create the group for the citizen
            group, created = Group.objects.get_or_create(name="Citizen")
            if created:
                perm = Permission.objects.get(codename="add_report")
                group.permissions.add(perm)
                group.save()

            return HttpResponseRedirect(redirect_url)
