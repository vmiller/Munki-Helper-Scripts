#!/usr/local/bin/managed_python3
#
# Written by Vaughn Miller
#
# 
# You should edit REPO_ROOT to reflect local path to the repo


import os
import subprocess
import plistlib
import sys

# =============================================================
# These variables should be edited for the intended environment
RECIPIENTS = ['user@domain.com']
SUBJECT = 'Munki Catalog Review'
REPO_ROOT = '/Volumes/its_munki_repo'
# =============================================================

# Build some paths using REPO_ROOT as a base
all_items_path = os.path.join(REPO_ROOT, 'catalogs', 'all')
catalogs_path = os.path.join(REPO_ROOT, 'catalogs')
pkgsinfo_path = os.path.join(REPO_ROOT, 'pkgsinfo')

# Build the path for the output file
script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
output_path = str(script_path) + '/results.txt'

# Before we get too far, lets check to make we can reach the catalog path
if not os.path.exists(all_items_path):
    print('\n*** ERROR : Catalogs not found at ' + str(catalogs_path) + ' ***')
    print('    Check to make sure the munki repo is mounted before running script')
    print('    And that makecatalogs has been run \n')
    quit()

# Read in all the catalog items
catalogitems = plistlib.readPlist(all_items_path)


diff = False
nameList = []
for item in catalogitems:
    # For every item in the repo get the list of catalogs, name, and version
    name = item.get('name')
    if name not in nameList:
        nameList.append(name)
        print(name)

    version = item.get('version')
    #print name + " :  " + version