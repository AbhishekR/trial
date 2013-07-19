#!/bin/bash
#install kvm
#sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils 
#sudo adduser `id -un` kvm
#sudo adduser `id -un` libvirtd
#sudo apt-get install virt-manager
#clone devstack 

git clone git://github.com/openstack-dev/devstack.git
#copy localrc file
cp ~/trial/localrc ~/trial/devstack/localrc
#install openstack
~/devstack/stack.sh
#copy all9s recovery module to openstack
cp -r ~/trial/recovery /opt/stack/horizon/openstack_dashboard/dashboards/project
#replacing the dashboard
rm /opt/stack/horizon/openstack_dashboard/dashboards/project/dashboard.py
rm /opt/stack/horizon/openstack_dashboard/static/dashboard/img/logo.png
rm /opt/stack/horizon/openstack_dashboard/static/dashboard/img/logo-splash.pn
cp ~/trial/logo.png /opt/stack/horizon/openstack_dashboard/static/dashboard//img/logo.png
cp ~/trial/logo.png /opt/stack/horizon/openstack_dashboard/static/dashboard/img/logo-splash.png
cp ~/dashboard.py /opt/stack/horizon/openstack_dashboard/dashboards/project
# restart the apache server
sudo service apache2 restart



