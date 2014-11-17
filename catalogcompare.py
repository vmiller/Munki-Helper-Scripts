#!/usr/bin/python
#
# Written by Vaughn Miller
#
# Simple script to comb the munki catalogs and list items missing from individual catalogs
# 
# 
# You should edit REPO_ROOT to reflect local path to the repo
# If using email option, you should edit RECIPIENTS to a list of valid email addresses to be notified
#
# Usage : 
# To Output to screen : ./catalogcompare.py -screen
# To send output to email : ./catalogcompare.py -email
#


import os
import subprocess
import plistlib
import sys

# =============================================================
# These variables should be edited for the intended environment
RECIPIENTS = ['user@domain.com']
SUBJECT = 'Munki Catalog Review'
REPO_ROOT = '/Volumes/munki_repo'
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
    print '\n*** ERROR : Catalogs not found at ' + str(catalogs_path) + ' ***'
    print '    Check to make sure the munki repo is mounted before running script'
    print '    And that makecatalogs has been run \n'
    quit()

# Read in all the catalog items
catalogitems = plistlib.readPlist(all_items_path)

# open up a file for the output
output_file = open(output_path, "w")

# build the list of catalogs excluding 'all'
master_catalog_list = []
for root, dirs, files in os.walk(catalogs_path):
    for file in files:
        if file != 'all':
            master_catalog_list.append(file)
output_file.write('---Found ' + str(len(master_catalog_list)) + ' catalogs---\n')
output_file.write(str(master_catalog_list) + '\n\n')

diff = False
for item in catalogitems:
    # For every item in the repo get the list of catalogs, name, and version
    item_catalogs = item.get('catalogs')
    name = item.get('name')
    version = item.get('version')
    
    # Check to see if each catalog in the master list of catalogs is a member of the 
    # list of catalogs for this item
    for catalog in master_catalog_list:
        if catalog not in item_catalogs:
            output_file.write('\n' + str(name) + ' ' + str(version) + ' missing from ' + str(catalog) + '\n')
            diff = True
            
            # Convert item name + version into a pkgsinfo filename
            item_plist = str(name) + '-' + str(version)
            
            # Walk the pkgsinfo directory to find the pkgsinfo file
            for root, dirs, files in os.walk(pkgsinfo_path):
                for file in files:
                    file_name = str(file)
                    if file_name.startswith(item_plist):
                        # Read in the pkgsinfo plist then grab the metadat Dict to print Date
                        plist_contents = plistlib.readPlist(os.path.join(root, file))
                        metadata = plist_contents.get('_metadata')
                        output_file.write('Added to repo : ' + str(metadata['creation_date']) + '\n')

if not diff:
    output_file.write('---All catalogs match---\n')

# close out the file
output_file.close()

if sys.argv[1] == '-email':
    # Send a notification email    
    for recipient in RECIPIENTS:
        subprocess.Popen(['/bin/mail', '-s', SUBJECT, recipient], \
         stdin=open(output_file, 'r'))
elif sys.argv[1] == '-screen':
    output_file=open(output_path, "r")
    print output_file.read()
else:
    print "Invalid Argument"