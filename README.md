## multiusersettingsgen.py ##
===========================
### usage ###
    $ multiusersettings.py path/to/spatialite/db.sqlite

This will print to STDOUT. To generate an xml file, pipe to
apppropriate location:

    $ multiusersettings.py path/to/spatialite/db.sqlite > drawinglife/data/appsettings.xml
### description ###
Script produces an xml file for use with [drawinglife animation]
(https://github.com/ptrv/drawinglife) in which multiple users are
entered.

See [crossing paths](http://planbperformance.net/index.php?id=crossingpaths) and
[day in the life](http://planbperformance.net/index.php?id=dayinlife) for examples of
projects made with this software.
