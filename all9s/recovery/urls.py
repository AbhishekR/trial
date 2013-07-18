from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

#from .views import AwesomeView
import openstack_dashboard
from .views import IndexView
from .views import LaunchView
from .views import PromoteView
from .views import CleanView
#import openstack_dashboard

urlpatterns = patterns(
    'openstack_dashboard.dashboards.project.recovery.views',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^launch/$', LaunchView.as_view(), name='launch'),
    url(r'^promote/$', PromoteView.as_view(), name='promote'),
    url(r'^clean/$', CleanView.as_view(), name='clean'),
    #url(r'^table$', AwesomeTableView.as_view(), name="table"),
)
