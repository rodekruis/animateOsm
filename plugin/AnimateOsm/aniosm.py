# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AnimateOsm
                                 A QGIS plugin
 Animates OSM changes within a time and bounding box.
                              -------------------
        begin                : 2017-09-05
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Netherlands Red Cross
        email                : rnijssen@rodekruis.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qgis.core import QgsMessageLog, Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
#from qgis.PyQt.QtCore import Qgis
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .aniosm_dockwidget import AnimateOsmDockWidget
import os.path


class AnimateOsm:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AnimateOsm_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Animate OSM')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AnimateOsm')
        self.toolbar.setObjectName(u'AnimateOsm')

        #print "** INITIALIZING AnimateOsm"

        self.pluginIsActive = False
        self.dockwidget = None

        self.do_log = True


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('AnimateOsm', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action



    def log(self, message, tab=u'animate osm'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)
            #progress.setText('  '+str(message))

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/AnimateOsm/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Animate OSM'),
            callback=self.run,
            parent=self.iface.mainWindow())


    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING AnimateOsm"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD AnimateOsm"

        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&Animate OSM'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING AnimateOsm"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = AnimateOsmDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)



            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
 
            self.dockwidget.pushButton_load.clicked.connect(self.load_layers)

            # set default datetimes
            self.dockwidget.dateTimeEdit_end.setDateTime(QDateTime.currentDateTime())
            self.dockwidget.dateTimeEdit_start.setDateTime(self.dockwidget.dateTimeEdit_end.dateTime().addDays(-7))


    def load_layers(self):
        self.log(u'start loading layers ...')
        overpass_query = self.get_overpass_query()
        self.log(overpass_query)

 
    def get_osm_data(self):
        pass


    def get_overpass_query(self):

        #Example Overpass Turbo query:
        '''
        [out:xml][timeout:25]
        [diff:"2018-03-16T15:00:00Z","2018-04-16T15:00:00Z"];
        (
          node["building"](17.99979487484851,-63.15679550170898,18.126112640728326,-62.99491882324219);
          way["building"](17.99979487484851,-63.15679550170898,18.126112640728326,-62.99491882324219);
          relation["building"](17.99979487484851,-63.15679550170898,18.126112640728326,-62.99491882324219);
          );
        (._;>;);
        out meta;
        '''

        start_time = self.dockwidget.dateTimeEdit_start.dateTime().toString('yyyy-MM-ddThh:mm:ssZ')
        end_time = self.dockwidget.dateTimeEdit_end.dateTime().toString('yyyy-MM-ddThh:mm:ssZ')
        bbox = self.get_overpass_bbox()

        result = '[out:xml][timeout:25]\n'
        result += '[diff:"%s","%s"];\n' % (start_time, end_time)
        result += '(\n'
        result += 'node["building"]%s;\n' % (bbox)
        result += 'way["building"]%s;\n' % (bbox)
        result += 'relation["building"]%s;\n' % (bbox)
        result += ');\n(._;>;);\nout meta;\n'

        return result



    def get_overpass_bbox(self):
        extent = self.iface.mapCanvas().extent()

        map_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
        wgs84_crs = QgsCoordinateReferenceSystem().fromEpsgId(4326)

        # transform if not wgs84
        if not map_crs == wgs84_crs:
            transform = QgsCoordinateTransform(map_crs, wgs84_crs, QgsProject.instance())
            extent = transform.transformBoundingBox(extent)


        result = '(%s, %s, %s, %s)' % (extent.yMinimum(), extent.xMinimum(), extent.yMaximum(), extent.xMaximum())  
        #self.log(result)
        return result
