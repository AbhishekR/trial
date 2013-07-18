import json
import httplib
import urllib
import urlparse
import logging
import sys

# weblib.py is the base library for the script_*.py files.
# It handles authentication with keystone, as well as
# providing several functions to facilitate HTTP requests.


### Get OpenStack Credentials

# change to False when you are using the test environment
usehttps = False

# Keystone service URL
keystoneURL = "localhost:5000"

## make sure that osuser is set to your actual username, "admin"
## works for test installs on virtual machines, but it's a hack
osuser = "admin"

## use something more secure than 'password'
ospassword = "password"
ostenant = "admin"

# Parameters for the upcoming POST
params1 = '{"auth":{"passwordCredentials":{"username":"%s", "password":"%s"}, "tenantName":"%s"}}'%(osuser, ospassword, ostenant)
# Headers for the POST
headers1 = {"Content-Type": "application/json"}

if (usehttps == True):
    # set key_file and cert_file to wherever the key and cert files
    # are located
    # We are disregarding this
    conn1 = httplib.HTTPSConnection(keystoneURL, key_file='../cert/priv.pem', cert_file='../cert/srv_test.crt')
else:
    # Make a new connection to keystone
    conn1 = httplib.HTTPConnection(keystoneURL)

# Make a POST
# "/v2.0/tokens" informs the server that we want authentication data
conn1.request("POST", "/v2.0/tokens", params1, headers1)

# Get the response
# response1 is a I/O stream.
response1 = conn1.getresponse()
# data1 is a string containing the contents of response1
# It is in standard JSON format.
data1 = response1.read()
# json.loads() loads a JSON formatted string into a python data structure (a dictionary).
dd1 = json.loads(data1)

# Close the connection
conn1.close()

# Grab the API token
# The API token is a string of random characters that authenticates our session
# It is included in the headers of any further requests so the server knows
#  that it's still the same client that is communicating
apitoken = dd1['access']['token']['id']


# Grab the service endpoints
# Different openstack services require different URL's to access them.
# This snippet extracts the ones we need for this script, nova and quantum.
# netloc is the IP and port in one string, like "10.0.0.3:4343"
# path is the extension that contains the API version (almost always v2.0)
#  and the tenant ID used to track which project is being used.
serviceCatalog = dd1["access"]["serviceCatalog"]
for e in serviceCatalog:
    if e["name"] == "nova":
        novaapiurlt = urlparse.urlparse(e["endpoints"][0]["publicURL"])
        novanetloc = novaapiurlt.netloc
        novapath = novaapiurlt.path
    elif e["name"] == "quantum":
        quantumapiurlt = urlparse.urlparse(e["endpoints"][0]['publicURL'])
        quantumnetloc = quantumapiurlt.netloc
        # For whatever reason, the default quantum path is just "/".
        # That causes errors, so we fixed it manually.
        #quantumpath = quantumapiurlt.path
        quantumpath = "/v2.0"
        
    # Here's cinder as well, just for kicks.
    elif e["name"] == "cinder":
        cinderapiurlt = urlparse.urlparse(e["endpoints"][0]['publicURL'])
        cindernetloc = cinderapiurlt.netloc
        cinderpath = cinderapiurlt.path


# Initialize the logger
L = logging.getLogger("script")
# Format for log files.
# Complete reference at http://docs.python.org/2/library/logging.html#logrecord-attributes
form = logging.Formatter("[%(asctime)s %(filename)s %(levelname)s]: %(message)s")

# Set up file writing for the logger
filehdlr = logging.FileHandler("script.log")
filehdlr.setFormatter(form)
L.addHandler(filehdlr)

# Set up console output for the logger
outhdlr = logging.StreamHandler(sys.stdout)
outhdlr.setFormatter(form)
L.addHandler(outhdlr)

# Set the logger to display info messages and worse
L.setLevel(logging.INFO)




# HTTP request functions
# These are the functions that enable simple HTTP requests.
# url is the IP and port to be used, usually one of novanetloc or quantumnetloc
# path is the path extension to be used, usually one of novapath or quantumpath
# ext is the last part of the path which represents which utility is
#  being accessed ("servers", "images", "networks", etc)
# POST also requires the body argument, which specifies additional information
#  to be transferred.

def get(url, path, ext):
    L.debug("GET %s%s/%s",url,path,ext)
    conn = httplib.HTTPConnection(url)
    conn.request("GET", path+"/"+ext, "", {"X-Auth-Token":apitoken, "Content-type":"application/json"})
    return conn.getresponse().read()

def post(url, path, ext, body):
    if type(body) == dict:
        body = json.dumps(body)
    L.debug("POST %s%s/%s",url,path,ext)
    L.debug("     %s", body)
    conn = httplib.HTTPConnection(url)
    conn.request("POST", path+"/"+ext, body, {"X-Auth-Token":apitoken, "Content-type":"application/json"})
    return conn.getresponse().read()

def delete(url, path, ext):
    L.debug("DELETE %s%s/%s",url,path,ext)
    conn = httplib.HTTPConnection(url)
    conn.request("DELETE", path+"/"+ext, "", {"X-Auth-Token":apitoken, "Content-type":"application/json"})
    return conn.getresponse().read()




