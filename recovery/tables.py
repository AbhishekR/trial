from horizon import tables

from django.utils.translation import ugettext_lazy as _

class DefaultTable(tables.DataTable):
    time = tables.Column("time", verbose_name=_("Date/Time"))
    source = tables.Column("source", verbose_name=_("Source"))
    level = tables.Column("level", verbose_name=_("Level"))
    message = tables.Column("message", verbose_name=_("Message"))



class Launch(tables.LinkAction):
    name = "launch"
    verbose_name = _("Launch Test Environment")
    url = "horizon:project:recovery:launch"
    classes = ("ajax-modal", "btn-edit")

class Promote(tables.LinkAction):
    name = "promote"
    verbose_name = _("Promote Test Environment")
    url = "horizon:project:recovery:promote"
    classes = ("ajax-modal", "btn-edit")

class Clean(tables.LinkAction):
    name = "clean"
    verbose_name = _("Remove Test Environment")
    url = "horizon:project:recovery:clean"
    classes = ("ajax-modal", "btn-edit")



class LaunchTable(DefaultTable):
    class Meta:
        name = "launch"
        verbose_name = _("Launch Table")
        table_actions = (Launch, Promote, Clean)
    
class PromoteTable(DefaultTable):
    class Meta:
        name = "promote"
        verbose_name = _("Promote Table")
        table_actions = (Launch, Promote, Clean)


class CleanTable(DefaultTable):
    class Meta:
        name = "clean"
        verbose_name = _("Clean Table")
        table_actions = (Launch, Promote, Clean)