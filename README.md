####A collection of scripts to help manage a Munki repository


**catalogcompare.py** - Looks for items that do not appear in all catalogs and provides a report.  It can output to the screen or send an email report.  The email functionality has only been testing in RHEL and Centos.  Your milage on other platforms may vary.

**manifestdependency.py** - Given a manifest, this script will report all other manifests that include it.