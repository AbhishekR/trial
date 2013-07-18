from weblib_meta import *
import script_cleanup_meta
import time

# script_promote.py takes existing instances running on an isolated instance
#  and publishes them to the public network.
def promote():
    L.info("Beginning promotion of temporary VMs...")
    
    instances = json.loads(get(novanetloc, novapath, "servers/detail"))["servers"]
    # demoVMS is a list of the names of instances that have demo* equivalents.
    # If a VM's name begins with the string "demo", then it is assumed that it was
    #  cloned from an existing published VM.
    # If we are promoting, then we are removing the original VM and replacing it
    #  with the demo VM.
    # demoVMS keeps tracks of which VM's must be deleted.
    demoVMS = []
    for instance in instances:
        if "demo" in instance["metadata"]:
            # Make sure the instance has finished building.
            if instance['OS-EXT-STS:vm_state'] == "building": L.info("Waiting for instance %s to finish building...", instance["name"])
            while instance['OS-EXT-STS:vm_state'] == "building":
                time.sleep(0.5)
                instance = json.loads(get(novanetloc, novapath, "servers/%s"%instance["id"]))["server"]
    
            if instance['OS-EXT-STS:vm_state'] != "active":
                L.error("Instance %s has state %s. It is assumed that this is problematic.", instance["name"], instance["OS-EXT-STS:vm_state"])
            
            demoVMS.append(instance["name"][5:])
    
            L.info("Shutting down instance %s...",instance["name"])
            post(novanetloc, novapath, "servers/%s/action"%instance["id"],{"os-stop":None})
            while instance['OS-EXT-STS:vm_state'] == "active":
                time.sleep(0.5)
                instance = json.loads(get(novanetloc, novapath, "servers/%s"%instance["id"]))["server"]
            L.info("Shut down instance %s", instance["name"])
            L.info("Snapshotting instance %s", instance["name"])
            post(novanetloc, novapath, "servers/%s/action"%instance["id"], {"createImage":{
                                                                                  "name":instance["name"],
                                                                                  "metadata":{"demo":"promotion"}
                                                                                  }})
    
    # Now that we have all the VMs we need to delete in demoVMS, we can delete them
    for instance in instances:
        if instance["name"] in demoVMS and (not "demo" in instance["metadata"]):
            name, id = instance["name"], instance["id"]
            L.info("Deleting instance %s (%s)", name, id)
            res = delete(novanetloc, novapath, "servers/%s"%instance["id"])
            if res != "": Log.error("DELETE call returned %s", res)
            instance = json.loads(get(novanetloc, novapath, "servers/%s"%id))
            # Wait until the instance is actually deleted before continuing
            while instance.has_key("server"):
                time.sleep(0.1)
                instance = json.loads(get(novanetloc, novapath, "servers/%s"%id))
            L.info(" Deleted instance %s (%s)", name, id)
    
    # We need the network ID of the public network.
    # We're just gonna assume that the public network is called public.
    networks = json.loads(get(quantumnetloc, quantumpath, "networks"))["networks"]
    for network in networks:
        if network["name"] == "public":
            netid = network["id"]
    
    # Go through all the images and instantiate the ones we just made.
    images = json.loads(get(novanetloc, novapath, "images/detail"))["images"]
    for image in images:
        if "demo" in image["metadata"] and image["metadata"]["demo"] == "promotion":
            if image["status"] == "SAVING": L.info("Waiting for image %s to finish saving...",image["name"])
            while image["status"] == "SAVING":
                time.sleep(0.5)
                image = json.loads(get(novanetloc, novapath, "images/%s"%image["id"]))["image"]
            L.info("Promoting image %s to production", image["name"])
            data = json.loads(post(novanetloc, novapath, "/servers", {"server":{
                                                                    "name":image["name"][5:],
                                                                    "imageRef":image["id"],
                                                                    "flavorRef":"1",
                                                                    "networks":[{"uuid":netid}]
                                                                    }}))["server"]
            print data
            L.info("New instance created: %s (%s)", image["name"], data["id"])
    
    script_cleanup_meta.clean()
    L.info("Promotion complete!")
  
if __name__ == "__main__":
    promote()






