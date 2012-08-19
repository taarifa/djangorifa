"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'project.menu.CustomMenu'
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    class Media:
        css = ('admin/css/admin-menu.css',)

    """
    Custom Menu for project admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Admin'), reverse('admin:index')),
            items.Bookmarks(),
            items.ModelList(
                _('Content'),
                models=(
                    'cms.models.pagemodel.*',
                    'media_tree.*',
                ),
            ),
            items.ModelList(
                _('Users'),
                models=('django.contrib.auth.*',)
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
