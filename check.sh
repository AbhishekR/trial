#!/bin/bash
#install kvm
#sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils 
#sudo adduser `id -un` kvm
#sudo adduser `id -un` libvirtd
#sudo apt-get install virt-manager
#clone devstack 
git clone git://github.com/openstack-dev/devstack.git
#install openstack
~/devstack ./stack.sh
#copy all9s recovery module to openstack
cp -r recovery /opt/stack/horizon/openstack_dashboard/dashboards/project
#replacing the dashboard
rm /opt/stack/horizon/openstack_dashboard/dashboards/project/dashboard.py
rm /opt/stack/horizon/openstack_dashboard/static/dashboard/logo.png
rm /opt/stack/horizon/openstack_dashboard/static/dashboard/logo-splash.pn
cp logo.png /opt/stack/horizon/openstack_dashboard/static/dashboard//img/logo.png
cp logo.png /opt/stack/horizon/openstack_dashboard/static/dashboard/img/logo-splash.png
cp dashboard.py /opt/stack/horizon/openstack_dashboard/dashboards/project
# restart the apache server
sudo service apache2 restart



