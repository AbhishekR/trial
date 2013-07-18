
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from horizon import forms
from horizon import messages
from horizon import exceptions

from scripts import script_cleanup_meta
from scripts import script_promote_meta
from scripts import script_create_meta

class LaunchEnvironment(forms.SelfHandlingForm):
    """
    name = forms.CharField(label=_("Name"),
                           error_messages={
                            'required': _('This field is required.'),
                            'invalid': _("The string may only contain"
                                         " ASCII characters and numbers.")},
                           validators=[validators.validate_slug])
    description = forms.CharField(label=_("Description"))
    """
    def handle(self, request, data):
        try:
            script_create_meta.create()
            messages.success(request,
                                _('Successfully launched the test environment!'))
            return True
        except Exception as e:
            messages.success(request, _("Error launching: %s"%e))

class CleanEnvironment(forms.SelfHandlingForm):
    """
    name = forms.CharField(label=_("Name"),
                           error_messages={
                            'required': _('This field is required.'),
                            'invalid': _("The string may only contain"
                                         " ASCII characters and numbers.")},
                           validators=[validators.validate_slug])
    description = forms.CharField(label=_("Description"))
    """
    def handle(self, request, data):
        #script_cleanup_meta.clean()
        try:
            script_cleanup_meta.clean()
            messages.success(request,
                                _('Successfully cleaned the test environment!'))
            return True
        except Exception as e:
            messages.success(request, _("Error cleaning: %s"%e))

class PromoteEnvironment(forms.SelfHandlingForm):
    """
    name = forms.CharField(label=_("Name"),
                           error_messages={
                            'required': _('This field is required.'),
                            'invalid': _("The string may only contain"
                                         " ASCII characters and numbers.")},
                           validators=[validators.validate_slug])
    description = forms.CharField(label=_("Description"))
    """
    def handle(self, request, data):
        #script_promote_meta.promote()
        try:
            script_promote_meta.promote()
            messages.success(request,
                                _('Successfully promoted the test environment!'))
            return True
        except Exception as e:
            messages.success(request, _("Error promoting: %s"%e))
        """
        try:
            sg = api.nova.security_group_create(request,
                                                data['name'],
                                                data['description'])
            messages.success(request,
                             _('Successfully created security group: %s')
                               % data['name'])
            return sg
        except:
            redirect = reverse("horizon:project:access_and_security:index")
            exceptions.handle(request,
                              _('Unable to create security group.'),
                              redirect=redirect)
            """


