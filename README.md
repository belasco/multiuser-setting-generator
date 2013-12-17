multiuser-setting-generator
===========================

# multiusersettingsgen.py #

## usage ##

$ multiusersettings.py path/to/spatialite/db.sqlite

This will print to STDOUT. To generate an xml file, pipe to
apppropriate location:

$ multiusersettings.py path/to/spatialite/db.sqlite > drawinglife/data/appsettings.xml

Script produces an xml file for use with drawinglife animation
(https://github.com/ptrv/drawinglife) in which multiple users are
entered.

See http://planbperformance.net/index.php?id=crossingpaths and
http://planbperformance.net/index.php?id=dayinlife for examples of
projects made with this software.
