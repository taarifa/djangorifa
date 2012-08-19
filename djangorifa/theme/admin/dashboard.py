"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'project.dashboard.CustomAppIndexDashboard'
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

        # Content administration
        """
        self.children.append(modules.Group(
            _('Content Administration'),
            display = 'stacked',
            force_show_title = False,
            children = [
                modules.ModelList(
                    show_title = False,
                    models = (
                        'cms.models.pagemodel.*',
                        'contact.models.*',
                        'tagging.models.*',
                    )
                ),
                modules.ModelList(
                    _('Photo Administration'),
                    models = (
                        'photologue.models.*',
                    ),
                ),
            ]
        ))
        self.children.append(modules.Group(
            _('Photo Administration'),
            children = [
                modules.ModelList(
                    _('Photos'),
                    models = (
                        'photologue.models.Photo',
                        'photologue.models.Gallery',
                        'photologue.models.GalleryUpload',
                    ),
                ),
                modules.ModelList(
                    _('Advanced'),
                    models = (
                        'photologue.models.PhotoSize',
                        'photologue.models.PhotoEffect',
                        'photologue.models.Watermark',
                    ),
                )
            ],
        ))
        """

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
