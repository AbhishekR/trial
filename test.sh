#!/bin/bash  
#copy all9s recovery module to openstack
cp -r recovery /opt/stack/horizon/openstack_dashboard/dashboards/project
#replacing the dashboard
rm /opt/stack/horizon/openstack_dashboard/dashboards/project/dashboard.py
cp dashboard.py /opt/stack/horizon/openstack_dashboard/dashboards/project
# restart the apache server
sudo service apache2 restart 



