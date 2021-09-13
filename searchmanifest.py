#!/usr/local/bin/managed_python3
#
# Written by Vaughn Miller
#
#
# Modify REPO_ROOT to match your environment

import os
import plistlib
import sys

#==== This should be modified to match your environment ====
REPO_ROOT = '/Volumes/its_munki_repo'
#-----------------------------------------------------------

manifest_path = os.path.join(REPO_ROOT, 'manifests')
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

def includesTitle(manifest, software, section):
    ''' given software title and manifest dict, check to see if 
    title is referenced. Returns true or false
    '''
    isReferenced = False

    try:
        with open(os.path.join(manifest_path, manifest), 'rb') as fp:
            manifest_plist = plistlib.load(fp)
        for title in manifest_plist.get(section):
            if title == software:
                isReferenced = True
    except:
        print("** Unable to load : " + manifest)        
    return isReferenced


# Before we get too far, lets check to make we can reach the manifest path
if not os.path.exists(manifest_path):
    print('\n*** ERROR : Manifests not found at ',str(manifest_path),' ***')
    print('    Check to make sure the munki repo is mounted before running script')
    quit()
    
# Walk the manifest path and build a list of manifests
manifest_list = []
for root, dirs, files in os.walk(manifest_path):
    for file in files:
        if str(file)[0] != '.':  # Ignore any dot files
            manifest_list.append(file)
    
# Get manifest from script argument and check for it's inclusions           
if len(sys.argv) == 3:
    softwareTitle = (sys.argv[1])
    manifestSection = (sys.argv[2])
else:
    print("**  Error - please provide title and manifest section ")
    exit(1)

for m in manifest_list:
    if includesTitle(m,softwareTitle, manifestSection):
        print(m + " has " + softwareTitle + " in  " + manifestSection)
