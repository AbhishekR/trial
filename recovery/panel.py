from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.project import dashboard


class Recovery(horizon.Panel):
    name = _("Recovery")
    slug = 'recovery'


dashboard.Project.register(Recovery)
