#!/usr/bin/env python
# -*- coding: utf-8 -*-

# multisettingsgen.py
# Started Sun 15 Dec 2013 13:37:50 CET
# danbelasco@yahoo.co.uk

# A utility script for use in conjunction with drawinglife
# openframeworks application (https://github.com/ptrv/drawinglife)

# After installing drawinglife and populating a spatialite database
# from gpx files using gpx2spatialite
# (https://github.com/ptrv/gpx2spatialite) - See the createdb.sh
# script in the extras folder to initiate a spatialite database.

# When making multiuser animations. Given a populated spatialite
# database (taken as only argument), generate an AppSettings.xml file
# for Peter's drawinglife animation. Prints to screen unless
# redirected to file (intended use).

# TODO:

# 1. make rgb random generate more distinct colours by
# generating in hsv first then converting
# http://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/

# Copyright (C) 2013 Daniel Belasco Rogers danbelasco@yahoo.co.uk

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.

import sys
from optparse import OptionParser
from datetime import datetime
try:
    from pyspatialite import dbapi2 as spatialite
except ImportError:
        print '*' * 48
        print "This script needs the python module pyspatialite"
        print
        print "You can get it from the repos"
        print "sudo apt-get install pyspatialite"
        print '*' * 48
        sys.exit(2)
try:
    import gpxpy.geo
except ImportError:
    print '*' * 48
    print 'This script needs the python module gpxpy to work'
    print
    print 'You can get it like so:'
    print 'sudo pip gpxpy'
    print 'Or install manually from pypi'
    print '*' * 48
    sys.exit(2)
from random import randrange
import os.path

TEMPLATE1 = """<?xml version="1.0" encoding="UTF-8"?>
<drawinglife>
  <data>
    <database>"""

TEMPLATE2 = """</database>
    <person>
"""

TEMPLATE3 = """  </person>
  </data>
<dbquery>
  <!-- There are four query types: -->
  <!-- 1 = day range -->
  <!-- 2 = month range -->
  <!-- 3 = year range -->
  <!-- 4 = city -->
  <!-- 5 = sql file for each person-->
  <type>3</type>
  <time>
    <yearstart>"""

TEMPLATE4 = """</yearstart>
    <yearend>"""

TEMPLATE5 = """</yearend>
  </time>
  <city></city>
</dbquery>
<settings>
  <loop>1</loop>
  <interactivemode>
    <enabled>0</enabled>
    <traced>1</traced>
  </interactivemode>
  <multimode>1</multimode>
  <multimodeinfo>1</multimodeinfo>
  <sleeptime>6</sleeptime>
  <usespeed threshold="10">0</usespeed>
  <log level="0" />
  <loadgpsonstart>1</loadgpsonstart>
  <debugmode>0</debugmode>
  <printvalues>1</printvalues>
  <fullscreen>0</fullscreen>
  <hidecursor>1</hidecursor>
  <showinfo>0</showinfo>
  <drawspeed>"""

TEMPLATE6 = """</drawspeed>
  <framerate>30</framerate>
  <!-- This sets the number of points to draw.-->
  <!-- To draw all points set 0 (very cpu intensive) -->
  <walklength>0</walklength>
  <boundingbox>
    <auto>1</auto>
    <static>0</static>
    <position lat='"""

TEMPLATE7 = "' lon='"

TEMPLATE8 = """'/>
    <size>"""

TEMPLATE9 = """</size>
    <padding>20.0</padding>
  </boundingbox>
  <meridian>
    <regions>1</regions>
    <region1 lon0="-119.0" minlon="-180.0" maxlon="-100.0" />
    <region2 lon0="-74.0" minlon="-100.0" maxlon="-35.0" />
    <region3 lon0="12.0" minlon="-35.0" maxlon="65.0" />
    <region4 lon0="116.0" minlon="65.0" maxlon="130.0" />
    <region5 lon0="146.0" minlon="130.0" maxlon="180.0" />
    <auto>1</auto>
    <!-- value in degrees -->
    <lon0>0.0</lon0>
  </meridian>
  <grabscreen>0</grabscreen>
</settings>
<ui>
  <fonts>
    <font name="mono.ttf" size="50" />
    <font name="mono.ttf" size="24" />
    <font name="mono.ttf" size="16" />
    <!-- <font name="Standard0753.ttf" size="8" /> -->
    <font name="consola.ttf" size="11" />
  </fonts>
  <alpha>
    <tracks>100</tracks>
    <legend>255</legend>
  </alpha>
  <color>
    <foreground r="255" g="255" b="255" />
    <background r="0" g="0" b="0" />
    <!-- <viewbox r="30" g="30" b="30" /> -->
    <interactiveseg r="255" g="255" b="0" a="255" />
  </color>
  <speedcolors>
    <underthreshold r="255" g="255" b="255" a="64" />
    <abovethreshold r="255" g="0" b="0" a="0" />
  </speedcolors>
  <imageascurrent>0</imageascurrent>
  <currentpointimages>
    <image>
      <path></path>
      <width></width>
      <height></height>
      <alpha></alpha>
    </image>
  </currentpointimages>
  <dotsize>5</dotsize>
  <locationimages>
    <!-- <image> -->
    <!--    <path>location_images/img.png</path> -->
    <!--    <name>test</name> -->
    <!--    <lat>52.47771</lat> -->
    <!--    <lon>-1.89857</lon> -->
    <!--    <width>24</width> -->
    <!--	<height>24</height> -->
    <!--	<alpha></alpha> -->
    <!--    <anchor> -->
    <!--   1 = percent, 2 = point-->
    <!--     <type>1</type> -->
    <!--     <posx>0.5</posx> -->
    <!--     <posy>0.5</posy> -->
    <!--     <show>0</show> -->
    <!--    </anchor> -->
    <!-- </image> -->
  </locationimages>
</ui>
<shader>
  <enabled>0</enabled>
  <vertex>noise.vert</vertex>
  <fragment>noise.frag</fragment>
</shader>
<zoomanimation>
  <active>0</active>                   <!--overrides bounding box-->
  <!-- 3 zoom types: -->
  <!-- 1 - specify time in animation where 0.0 is the beginning and 1.0 the end -->
  <!-- 2 - specify a gpsid from database -->
  <!-- 3 - specify a timestamp from database in iso 8601 format -->
  <type>1</type>
  <frames>
   <frame time="0.0" timestamp="" gpsid="" zoom="15000" lat="52.49734" lon="13.44594"/>
   <frame time="0.05" timestamp="" gpsid="" zoom="1000" lat="52.49757" lon="13.44524"/>
   <frame time="0.1" timestamp="" gpsid="" zoom="1000" lat="52.49686" lon="13.4452"/>
   <frame time="0.2" timestamp="" gpsid="" zoom="10000" lat="52.49734" lon="13.44594"/>
   <frame time="0.3" timestamp="" gpsid="" zoom="2000" lat="52.49734" lon="13.44594"/>
   <frame time="0.4" timestamp="" gpsid="" zoom="15000" lat="52.49734" lon="13.44594"/>
   <frame time="0.5" timestamp="" gpsid="" zoom="3000" lat="52.49734" lon="13.44594"/>
   <frame time="0.6" timestamp="" gpsid="" zoom="11000" lat="52.49734" lon="13.44594"/>
  </frames>
  <!-- tweening parameters -->
  <!-- z tweening -->
  <dampzoom>0.3</dampzoom>
  <attractionzoom>0.08</attractionzoom>
  <!-- xy tweening -->
  <dampcenter>0.2</dampcenter>
  <attractioncenter>0.2</attractioncenter>
</zoomanimation>
<sound>
  <active>0</active>
  <soundfiles>
    <!-- <soundfile src="test1.mp3"/> -->
    <!-- <soundfile src="test2.mp3"/> -->
  </soundfiles>
</sound>
</drawinglife>"""


def parseargs():
    """
    Parses the arguments and options the user called the script with
    database is set to theGPSdatabase by default but can be changed
    with the -d option
    """
    usage = """%prog path/to/database
Intended use is to pipe output to a settings file:
%prog /path/to/database.sqlite > settings.xml
Otherwise, the output is printed to STDOUT"""
    parser = OptionParser(usage, version="%prog 0.1")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("""Please enter a path to a database
""")
    dbpath = args[0]
    return dbpath


def isotodatetime(isodate):
    """
    take an iso format date and transform into a python datetime
    object.

    This is the builtiin way of doing it that might be slower,
    but is much better than the below. Here it is for reference
    """
    outputdate = datetime.strptime(isodate, "%Y-%m-%d %H:%M:%S")
    return outputdate


def getsql(dbpath, sql):
    """
    Generic query database function
    """
    conn = spatialite.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def readusersdb(dbpath):
    """
    connect to the database and get a list of users
    """
    sql = """SELECT username FROM 'users'
ORDER BY 'user_uid'"""
    data = getsql(dbpath, sql)
    return data


def getyearrange(dbpath):
    """
    get a the startyear and endyear for the settings xml based on min
    and max years from file table
    """
    sql = """SELECT MIN("first_timestamp"), MAX("last_timestamp")
FROM 'files'"""
    data = getsql(dbpath, sql)
    yearstart = isotodatetime(data[0][0])
    yearend = isotodatetime(data[0][1])
    return str(yearstart.year), str(yearend.year)


def getcentres(dbpath):
    """
    get the lat lon centrepoint of all tracks to centre the animation
    using a spatialite sql
    """
    sql = "SELECT MIN(X(geom)), MAX(X(geom)), MIN(Y(geom)), MAX(Y(geom)) "
    sql += "FROM 'trackpoints'"
    data = getsql(dbpath, sql)
    minlon = data[0][0]
    maxlon = data[0][1]
    minlat = data[0][2]
    maxlat = data[0][3]
    centrelat = (minlat + maxlat) / 2
    centrelon = (minlon + maxlon) / 2
    # calculate the distance between the latitudes to estimate the
    # zoom size using the gpxpy.geo module
    zoom = gpxpy.geo.distance(minlat, minlon, None, maxlat, minlon, None)
    zoom += 400  # a buffer so that the lines do not go off screen
    return centrelat, centrelon, zoom


def persongenerator(userlist):
    """
    iterate through the list of users and generate the name tags for
    the settings xml
    """
    namelist = ""
    for name in userlist:
        r = randrange(0, 255)
        g = randrange(0, 255)
        b = randrange(0, 255)
        namelist += '    <name r="%d' % r
        namelist += '" g="%d' % g
        namelist += '" b="%d' % b
        namelist += '" a="200" sql="example.sql">'
        namelist += name[0]
        namelist += '</name>\n'
    return namelist


def main():
    """
    run everything - should look like pseudocode
    """
    dbpath = parseargs()
    userlist = readusersdb(dbpath)
    namelist = persongenerator(userlist)
    db = os.path.basename(dbpath)
    yearstart, yearend = getyearrange(dbpath)
    centrelat, centrelon, zoom = getcentres(dbpath)
    print TEMPLATE1 + db + TEMPLATE2 + namelist + TEMPLATE3 + yearstart\
      + TEMPLATE4 + yearend + TEMPLATE5 + str(len(userlist)) + TEMPLATE6\
      + str(centrelat) + TEMPLATE7 + str(centrelon) + TEMPLATE8 + str(zoom)\
      + TEMPLATE9


if __name__ == '__main__':
    sys.exit(main())
