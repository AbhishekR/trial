
from weblib_meta import *
import logging
import sys

import xml.etree.cElementTree as ET
from xml.dom import minidom
import time

# script_create.py takes a number of existing instances, snapshots them,
#  and duplicates them on an isolated network.
def create():
    L.info("Beginning temporary server creation...")
    
    L.info("Updating conf.xml...")
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")
    
    # Gets the list of all instances
    servers = json.loads(get(novanetloc, novapath, "servers"))["servers"]
    i = 0
    for s in servers:
            i += 1
            L.info("    adding server %s (%s)", s["name"], s["id"])
            # Add a new <vm> tag
            vmField = ET.SubElement(doc, "vm" + str(i))
            ET.SubElement(vmField, "id").text = s["id"]
            ET.SubElement(vmField, "name").text = s["name"]
    
    tree = ET.ElementTree(root)
    tree.write("conf.xml")
    L.info("conf.xml updated to current servers")
    
    L.info("Reading conf.xml...")
    # parsing xml file
    xmldoc = minidom.parse('conf.xml')
    grammarNode = xmldoc.firstChild
    child = grammarNode.firstChild
    
    if len(child.childNodes) == 0:
        L.info("No instances! Exiting :(")
        return
    
    for vm in child.childNodes:
        name = vm.getElementsByTagName("name")[0].firstChild.data
        id = vm.getElementsByTagName("id")[0].firstChild.data
        post(novanetloc, novapath, "servers/%s/action" % id, {"createImage":{
                                                                           "name":name,
                                                                           "metadata":{
                                                                                       "demo":"create"
                                                                                       }
                                                                           }})
        L.info("    Created image %s of instance %s (%s)", name, name, id)
    
    
    # Creating isolated network
    # Apparently if you create a new network with default settings, it's isolated.
    net = post(quantumnetloc, quantumpath, "networks", {"network":
                                                                            {
                                                                             "name": "demo_network",
                                                                             }})
    net = json.loads(net)["network"]
    netid = net["id"]
    L.info("Created new network %s (%s)", net["name"], netid)
    nets1 = get(quantumnetloc, quantumpath, "subnets")
    #print nets
    sub = post(quantumnetloc, quantumpath, "subnets", {"subnet":{
                                                                   "network_id":netid,
                                                                   "ip_version":4,
                                                                   "cidr":"10.0.3.0/24",
                                                                   "allocation_pools":[{
                                                                                        "start":"10.0.3.20",
                                                                                        "end":"10.0.3.150"
                                                                                        }]
                                                                   }
                                                         })
    
    
    L.info("Created new subnet on 10.0.3.0/24")
    
    # Launch instances of the new images on the new network
    # flavor is the size of the vm (tiny, small, large, etc)
    # We are using tiny.
    flavor = json.loads(get(novanetloc, novapath, "flavors"))["flavors"][0]["id"]
    # Get all images
    images = json.loads(get(novanetloc, novapath, "images/detail"))["images"]
    for image in images:
        # If it's not one of our images, ignore it
        image = json.loads(get(novanetloc, novapath, "images/%s"%image["id"]))["image"]
        if not "demo" in image["metadata"]:
            continue
        if image["metadata"]["demo"] != 'create':
            continue
        if image["status"] == "SAVING":
            L.info("Waiting for image %s to finish saving...", image["name"])
        while image["status"] == "SAVING":
            time.sleep(0.5)
            image = json.loads(get(novanetloc, novapath, "images/%s"%image["id"]))["image"]
        L.info("Starting new server %s from image %s","test_"+image["name"], image["name"])
        data = json.loads(post(novanetloc, novapath, "servers", {"server":{
                                                                           "flavorRef":flavor,
                                                                           "imageRef":image["id"],
                                                                           "name":"test_"+image["name"],
                                                                           "networks":[{"uuid":netid}],
                                                                           "metadata":{"demo":"demo"}                                                                   }}))
        data = json.loads(get(novanetloc, novapath, "servers/%s"%data["server"]["id"]))["server"]
        if data["OS-EXT-STS:vm_state"] == "building":
            L.info("Waiting for instance %s to finish building...", data["name"])
        while data["OS-EXT-STS:vm_state"] == "building":
            time.sleep(0.1)
            data = json.loads(get(novanetloc, novapath, "servers/%s"%data["id"]))["server"]
        L.info(" Started server %s", data["name"])
    L.info("Creation complete!")
    # print get(quantumnetloc, "", "tenants/%s/networks.xml"%tenantID)

if __name__ == "__main__":
    create()

