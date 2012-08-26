"""
Defines the layout of the admin homepage
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

class CustomDashboard(Dashboard):
    """
    Custom index dashboard for project.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # Facilities Admin
        self.children.append(modules.ModelList(
            _('Facility Administration'),
            models = ('facilities.models.*',)
        ))

        # Reports Admin
        self.children.append(modules.ModelList(
            _('Reports Administration'),
            models = ('reports.models*',),
        ))

        # User administration
        self.children.append(modules.ModelList(
            _('User Administration'),
            models = ('django.contrib.auth.*',),
        ))

        self.children.append(modules.Group(
            _('Configuration'),
            display='tabs',
            children=[
                modules.LinkList(
                    title = 'Wizard',
                    children = [[_('Run configuration wizard'), reverse('taarifa_config:setup')]],
                ),
                # TODO Need individual view to facilities upload
                modules.ModelList(
                    title = 'Individual',
                    models = ('taarifa_config.models.*', 'django.contrib.sites.models.*'),
                )
            ]
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'), 5,
            layout='inline',
        ))

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for project.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
