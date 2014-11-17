#!/usr/bin/python
#
# Written by Vaughn Miller
#
# Playing around with Munki manifest dependencies 
#
# Modify REPO_ROOT to match your environment

import os
import plistlib
import sys

#==== This should be modified to match your environment ====
REPO_ROOT = '/Volumes/munki_repo'
#-----------------------------------------------------------

manifest_path = os.path.join(REPO_ROOT, 'manifests')
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))


def includedByManifests(manifest):
    global included_list
    for m in manifest_list:
        manifest_plist = plistlib.readPlist(os.path.join(manifest_path, m))
        included_manifests = manifest_plist.get('included_manifests')
        if manifest in included_manifests:
            includedByManifests(m)
            included_list = included_list + [m]

def includesManifests(manifest):
    manifest_plist = plistlib.readPlist(os.path.join(manifest_path, manifest))
    return list(manifest_plist.get('included_manifests'))

# Before we get too far, lets check to make we can reach the manifest path
if not os.path.exists(manifest_path):
    print '\n*** ERROR : Manifests not found at ' + str(manifest_path) + ' ***'
    print '    Check to make sure the munki repo is mounted before running script'
    quit()
    
# Walk the manifest path and build a list of manifests
manifest_list = []
for root, dirs, files in os.walk(manifest_path):
    for file in files:
        if str(file)[0] != '.':  # Ignore any dot files
            manifest_list.append(file)
    
# Get manifest from script argument and check for it's inclusions           
if len(sys.argv) == 2:
    
    includes = includesManifests(sys.argv[1])
    if includes != []:
        print str(sys.argv[1]) + ' includes : '
        for item in includes:
            print '        ' + str(item)
            
    included_list = []
    includedByManifests(sys.argv[1])
    if included_list != []:
        print str(sys.argv[1]) + ' included by : ' 
        for item in included_list:
            print '                   ' + item
    else:
        print str(sys.argv[1]) + ' not included in any manifests\n'
else:
    print "Error : provide just one argument"