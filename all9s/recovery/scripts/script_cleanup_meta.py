from weblib_meta import *
import time

# script_cleanup.py simply removes any unneeded resources.
# It also provides the functions necessary for other scripts
#  (like script_promote.py) to do likewise


def cleanInstances():
    instances = json.loads(get(novanetloc, novapath, "servers/detail"))["servers"]
    for instance in instances:
        if "demo" in instance["metadata"]:
            name = instance["name"]
            id = instance["id"]
            L.info("Deleting instance %s (%s)", name, id)
            res = delete(novanetloc, novapath, "servers/%s"%instance["id"])
            if res != "": Log.error("DELETE call returned %s", res)
            instance = json.loads(get(novanetloc, novapath, "servers/%s"%id))
            # Wait until the instance is actually deleted before continuing
            while instance.has_key("server"):
                time.sleep(0.1)
                instance = json.loads(get(novanetloc, novapath, "servers/%s"%id))
            L.info(" Deleted instance %s (%s)", name, id)

def cleanImages():
    snapshots = json.loads(get(novanetloc, novapath, "images/detail"))["images"]
    for snap in snapshots:
        if "metadata" in snap and "demo" in snap["metadata"]:
            L.info("Deleting image %s (%s)", snap["name"], snap["id"])
            res = delete(novanetloc, novapath, "images/%s"%snap["id"])
            if res != "": Log.error("DELETE call returned %s", res)
            L.info(" Deleted image %s (%s)", snap["name"], snap["id"])

def cleanNetworks():
    networks = json.loads(get(quantumnetloc, quantumpath, "networks"))["networks"]
    for network in networks:
        if network["name"] == "demo_network":
            L.info("Deleting network %s (%s)", network["name"], network["id"])
            res = delete(quantumnetloc, quantumpath, "networks/"+network["id"])
            if res != "": Log.error("DELETE call returned %s", res)
            L.info(" Deleted network %s (%s)", network["name"], network["id"])


def cleanSubnets():
    subnets = json.loads(get(quantumnetloc, quantumpath, "subnets"))["subnets"]
    print subnets
    for subnet in subnets:
        if isNamed(subnet, named):
            L.info("Deleting subnet %s (%s)", subnet["name"], subnet["id"])
            res = delete(quantumnetloc, quantumpath, "subnets/"+subnet["id"])
            if res != "": Log.error("DELETE call returned %s", res)
            L.info(" Deleted subnet %s (%s)", subnet["name"], subnet["id"])
        
def clean():
    L.info("Beginning cleanup of unnecessary resources...")
    cleanInstances()
    cleanImages()
    cleanNetworks()
    L.info("Cleanup completed.")

if __name__ == "__main__":
    clean()


