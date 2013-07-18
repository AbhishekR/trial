

from django.utils.translation import ugettext_lazy as _
from horizon import tabs
from .tables import LaunchTable
from .tables import PromoteTable
from .tables import CleanTable

class LaunchTab(tabs.TableTab):
    table_classes = (LaunchTable,)
    name = _("Launch")
    slug = "launchtab"
    template_name = ("horizon/common/_detail_table.html")

    def get_launch_data(self):
        return []
    #def get_context_data(self, request):
    #    return {"instance": self.tab_group.kwargs['instance']}

class PromoteTab(tabs.TableTab):
    table_classes = (PromoteTable,)
    name = _("Promote")
    slug = "promotetab"
    template_name = ("horizon/common/_detail_table.html")

    def get_promote_data(self):
        return []
        #return [{"time":"now","source":"me","level":"flat","message":"Yeah!"}]
    
class CleanTab(tabs.TableTab):
    table_classes = (CleanTable,)
    name = _("Clean")
    slug = "cleantab"
    template_name = ("horizon/common/_detail_table.html")

    def get_clean_data(self):
        return []

class AllTheTabs(tabs.TabGroup):
    slug = "instance_details"
    tabs = (LaunchTab, PromoteTab, CleanTab)
    sticky = True