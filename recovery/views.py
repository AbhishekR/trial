
#from django.views.generic import TemplateView
#from django.utils.datastructures import SortedDict
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from horizon import tabs
from horizon import forms
from .forms import LaunchEnvironment
from .forms import PromoteEnvironment
from .forms import CleanEnvironment
#from horizon import exceptions
#from openstack_dashboard import api
from .tabs import AllTheTabs

class IndexView(tabs.TabbedTableView):
    tab_group_class = AllTheTabs
    template_name = 'project/recovery/index.html'

class LaunchView(forms.ModalFormView):
    form_class = LaunchEnvironment
    template_name = 'project/recovery/launch.html'
    success_url = reverse_lazy('horizon:project:network_topology:index')
class PromoteView(forms.ModalFormView):
    form_class = PromoteEnvironment
    template_name = 'project/recovery/promote.html'
    success_url = reverse_lazy('horizon:project:network_topology:index')
class CleanView(forms.ModalFormView):
    form_class = CleanEnvironment
    template_name = 'project/recovery/clean.html'
    success_url = reverse_lazy('horizon:project:network_topology:index')

"""
class RecoveryTableView(tables.DataTableView):
    table_class = RecoveryInstancesTable
    template_name = 'project/recovery/index.html'
    
    def has_more_data(self, table):
        return self._more
    
    def get_data(self):
        marker = self.request.GET.get(
                        RecoveryInstancesTable._meta.pagination_param, None)
        # Gather our instances
        try:
            instances, self._more = api.nova.server_list(
                                        self.request,
                                        search_opts={'marker': marker,
                                                     'paginate': True})
        except:
            self._more = False
            instances = []
            exceptions.handle(self.request,
                              _('Unable to retrieve instances.'))
        # Gather our flavors and correlate our instances to them
        if instances:
            print "\n\n\n\n\n\n"
            print instances
            print "\n\n\n\n\n\n"
            try:LaunchView
                flavors = api.nova.flavor_list(self.request)
            except:
                flavors = []
                exceptions.handle(self.request, ignore=True)

            full_flavors = SortedDict([(str(flavor.id), flavor)
                                        for flavor in flavors])
            # Loop through instances to get flavor info.
            for instance in instances:
                try:
                    flavor_id = instance.flavor["id"]
                    if flavor_id in full_flavors:
                        instance.full_flavor = full_flavors[flavor_id]
                    else:
                        # If the flavor_id is not in full_flavors list,
                        # get it via nova api.
                        instance.full_flavor = api.nova.flavor_get(
                            self.request, flavor_id)
                except:
                    msg = _('Unable to retrieve instance size information.')
                    exceptions.handle(self.request, msg)
        return instances
"""