.. AnimateOsm documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AnimateOsm's documentation
==========================

This plugin creates animation frame images for changes in OpenStreetMap (OSM) data. You
can either download the changes from an OSM Overpass Turbo server or open a *.osm file
containing these changes. 

Input data
==========

Download
--------
Most convenient method is:

- zoom in to your desired area
- set date/time for Start and End of the period
- press "Download data"

The data will be downloaded from:

https://lz4.overpass-api.de/api/interpreter/

In case the plugin download fails, usually caused by a network time out, you can try to
manualy download the data from an(other) overpass server. Your query will look like this:

::

  [out:xml][timeout:60]
  [diff:"2018-06-06T13:00:00Z","2018-06-13T14:00:00Z"];
  (
    node["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);
    way["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);
    relation["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);
  );
  (._;>;);
  out meta geom;

You can use any Overpass Turbo server, for example:

https://overpass-turbo.eu/

The downloaded osm file can be saved as <filename>.osm and loaded using the Open file button.

File
----
In case you already downloaded an osm diff file, you can open it using the "Open file..."
button. The data will be parsed and the data/time settings will be updated accordingly.

Frames
======

Define the frame duration by setting the value in hours from 1 up to 48. The slider will
be set accordingly. You can use the slider to update the map. In case of large files this
can take a (few) second(s).

You can change the layer style by picking another Layer style in the Output group, or
define your own style using standard QGIS functionality. 

Output
======

Save all you frames as png images using the "Export images" button. You can define the
output directory and image size. **All existing images in that directory will be deleted
before the export starts!**

Use any video editing tool to convert your images to a real animation. (Unfortunately,
since QGIS runs on many OS platforms, it is really hard to automate this step :( )

Development
===========

This plugin has been developed by 510, a data initiative of the Netherlands Red Cross.
The main goal is creating animations for Missing Maps events (e.g. mapathons).

.. image:: 510_logo_linear.png

`www.510.global <https://www.510.global/>`_

`www.openstreetmap.org <https://www.openstreetmap.org/>`_

If you have any suggestions for this plugin or meet any bugs, please file them on
github:

https://github.com/rodekruis/animateOsm/issues


