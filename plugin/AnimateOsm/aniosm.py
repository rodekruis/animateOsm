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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QDateTime, QVariant, QSize
from PyQt5.QtGui import QIcon, QImage, QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QFileDialog, QProgressBar
from qgis.core import QgsMessageLog, Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, \
    QgsVectorLayer, QgsField, QgsProject, QgsFeature, QgsGeometry, QgsMapRendererSequentialJob, QgsMapSettings
from qgis.gui import QgsFileWidget
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
from .aniosm_dockwidget import AnimateOsmDockWidget
import os.path
from math import floor, ceil
import time

from .osm_diff import OsmDiffParser, download_osm_diff



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
        self.polygon_layer = None

        self.open_file_dialog = QFileDialog()
        self.open_file_dialog.setDirectory('/home/raymond/git/animateOsm/plugin/AnimateOsm/data')
        self.choose_dir_dialog = QFileDialog()
        self.choose_dir_dialog.setDirectory('/home/raymond/tmp/osmani')


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
 
            # set default datetimes
            self.dockwidget.dateTimeEdit_start.setDateTime(QDateTime.currentDateTime().addDays(-40))
            self.dockwidget.dateTimeEdit_end.setDateTime(QDateTime.currentDateTime())
            # for testing 08-09-17 19:57
            #test_start_date = QDateTime.fromMSecsSinceEpoch(1504592079000)
            #test_end_date = QDateTime.fromMSecsSinceEpoch(1507918747000)

            #test_end_date = QDateTime.fromString('08-09-17 19:57',self.dockwidget.dateTimeEdit_end.displayFormat())
            #self.dockwidget.dateTimeEdit_start.setDateTime(test_start_date)
            #self.dockwidget.dateTimeEdit_end.setDateTime(test_end_date)


            # connections
            self.dockwidget.pushButton_open_file.clicked.connect(self.select_and_open_file)
            self.dockwidget.pushButton_download.clicked.connect(self.download_and_open_file)
            
            self.dockwidget.dateTimeEdit_start.dateTimeChanged.connect(self.update_interval)
            self.dockwidget.dateTimeEdit_end.dateTimeChanged.connect(self.update_interval)
            self.dockwidget.spinBox_duration.valueChanged.connect(self.update_interval)

            self.dockwidget.horizontalSlider_frames.valueChanged.connect(self.update_slider)

            self.dockwidget.toolButton_choose_output_dir.clicked.connect(self.update_select_output_dir)
            self.dockwidget.pushButton_export.clicked.connect(self.export_frames)

            self.update_interval()


    def select_and_open_file(self):
        #Opens the file dialog to pick a file to open
        file_name = self.open_file_dialog.getOpenFileName(caption = "Open osm diff file", filter = '*.osm')
        self.log(file_name[0])
        if not os.path.isfile(file_name[0]):
            return
        self.open_file(file_name[0], update_extents=True)

        if len(self.parser.ways) == 0:
            self.log('No ways')
            return
        
        self.dockwidget.dateTimeEdit_start.setDateTime(self.__get_qdatetime(self.parser.min_timestamp))
        self.dockwidget.dateTimeEdit_end.setDateTime(self.__get_qdatetime(self.parser.max_timestamp))
        self.update_slider()



    def download_and_open_file(self):
        #Downloads the osm diff and opens the layer(s)

        # todo: Make more dynamic filename
        file_name = '/home/raymond/git/animateOsm/plugin/AnimateOsm/data/diff2.osm'

        overpass_query = self.get_overpass_query()
        self.log(overpass_query)

        self.show_progress()

        #encode to bytes
        overpass_query = overpass_query.encode()

        download_osm_diff(self, overpass_query, file_name)

        self.open_file(file_name, update_extents=True)

        self.iface.messageBar().clearWidgets()

    def update_select_output_dir(self):
        # opens a file selector
        file_name = self.choose_dir_dialog.getExistingDirectory(caption = "Choose output directory")#, QFileDialog.ShowDirsOnly)
        self.dockwidget.lineEdit_output_dir.setText(file_name)


    def __get_qdatetime(self, py_datetime):
        epoch = time.mktime(py_datetime)
        self.log(epoch)
        result = QDateTime.fromMSecsSinceEpoch(epoch * 1000)
        self.log(result)
        return result


    

    def open_file(self, file_name, update_extents=False):
        self.create_memory_layer()

        self.parser = OsmDiffParser()
        #parser.read(os.path.join(self.plugin_dir, 'data', 'diff.osm'))
        self.parser.read(file_name)
        self.log(self.parser)

        if len(self.parser.ways) == 0:
            self.log('no ways in file')
            return

        for way in self.parser.ways:
            self.add_polygon(self.parser.ways[way])
        self.polygon_layer.updateExtents()

        if update_extents:
            # only when loading  layer from file
            map_extent = self.polygon_layer.extent()

            map_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
            wgs84_crs = QgsCoordinateReferenceSystem().fromEpsgId(4326)

            # transform if not wgs84
            if not map_crs == wgs84_crs:
                transform = QgsCoordinateTransform(wgs84_crs, map_crs, QgsProject.instance())
                self.data_zoom_extent = transform.transformBoundingBox(map_extent)
            else:
                self.data_zoom_extent = map_extent

            self.iface.mapCanvas().setExtent(self.data_zoom_extent)

        self.iface.mapCanvas().refreshAllLayers()

        self.parser.reset_time_range()
        self.log(self.parser.min_timestamp)
        self.log(self.parser.max_timestamp)

        # TODO: create polygon and linestring layers, or even buildings, roads etc...


    def load_layers(self):
        self.log(u'start loading layers ...')

        
        # TODO: download data and store as data/diff.osm







    def update_interval(self):
        self.interval_msecs = self.dockwidget.spinBox_duration.value() * 3600000
        
        start_time_msecs = self.dockwidget.dateTimeEdit_start.dateTime().toMSecsSinceEpoch()
        animation_start_time_msecs = floor(start_time_msecs / self.interval_msecs) * self.interval_msecs
        self.animation_start_time = QDateTime.fromMSecsSinceEpoch(animation_start_time_msecs)

        end_time_msecs = self.dockwidget.dateTimeEdit_end.dateTime().toMSecsSinceEpoch()
        animation_end_time_msecs = ceil(end_time_msecs / self.interval_msecs) * self.interval_msecs
        self.animation_end_time = QDateTime.fromMSecsSinceEpoch(animation_end_time_msecs)

        number_of_frames = round((animation_end_time_msecs - animation_start_time_msecs) / self.interval_msecs) + 1

        self.dockwidget.label_animation_start.setText(self.animation_start_time.toString(self.dockwidget.dateTimeEdit_start.displayFormat()))
        self.dockwidget.label_animation_end.setText(self.animation_end_time.toString(self.dockwidget.dateTimeEdit_end.displayFormat()))
        self.dockwidget.label_frames.setText(u'%s frames' % number_of_frames)

        self.dockwidget.horizontalSlider_frames.setMinimum(1)
        self.dockwidget.horizontalSlider_frames.setMaximum(number_of_frames)
        self.dockwidget.horizontalSlider_frames.setValue(number_of_frames)




 


    def get_overpass_query(self):

        #Example Overpass Turbo query:
        '''
        q[out:xml][timeout:60]
        [diff:"2018-06-06T13:00:00Z","2018-06-13T14:00:00Z"];(\
            node["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);\
            way["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);\
            relation["building"](18.02701338, -63.08376483, 18.02811712, -63.08006941);\
            );\
        (._;>;);\
        out meta geom;'
        '''

        start_time = self.animation_start_time.toString('yyyy-MM-ddThh:mm:ssZ')
        end_time = self.animation_end_time.toString('yyyy-MM-ddThh:mm:ssZ')
        bbox = self.get_overpass_bbox()

        result = u'[out:xml][timeout:60]\n'
        result += u'[diff:"%s","%s"];\n' % (start_time, end_time)
        result += u'(\n'
        result += u'node["building"]%s;\n' % (bbox)
        result += u'way["building"]%s;\n' % (bbox)
        result += u'relation["building"]%s;\n' % (bbox)
        result += u');\n(._;>;);\nout meta geom;\n'

        return result



    def get_overpass_bbox(self):
        extent = self.iface.mapCanvas().extent()

        map_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
        wgs84_crs = QgsCoordinateReferenceSystem().fromEpsgId(4326)

        # transform if not wgs84
        if not map_crs == wgs84_crs:
            transform = QgsCoordinateTransform(map_crs, wgs84_crs, QgsProject.instance())
            extent = transform.transformBoundingBox(extent)

        result = u'(%s, %s, %s, %s)' % (
            round(extent.yMinimum(), 8),
            round(extent.xMinimum(), 8),
            round(extent.yMaximum(), 8),
            round(extent.xMaximum(), 8))
        return result



    def create_memory_layer(self, feature_type=u'polygon'):
        layer_name = u'osm_diff_%ss' % (feature_type)
        
        # delete existing layers
        layers = QgsProject.instance().mapLayersByName(layer_name)
        for layer in layers:
            QgsProject.instance().removeMapLayer(layer.id())

        feature_type += u'?crs=epsg:4326'
        self.polygon_layer = QgsVectorLayer(feature_type, layer_name, 'memory')
        self.polygon_provider = self.polygon_layer.dataProvider()

        osm_id_field = QgsField("osm_id", QVariant.LongLong, 'int8')
        user_field = QgsField("user", QVariant.String)
        user_field.setLength(80)
        timestamp_field = QgsField("timestamp", QVariant.DateTime)
        epoch_field = QgsField("epoch", QVariant.LongLong, 'int8')
        age_field = QgsField("frame_age", QVariant.Int)


        self.polygon_provider.addAttributes([osm_id_field, user_field, timestamp_field, epoch_field, age_field])
        self.polygon_layer.updateFields()

        QgsProject.instance().addMapLayer(self.polygon_layer)

        polygonQml = os.path.join(self.plugin_dir,'data','ani_osm_polygon_pink.qml')
        self.polygon_layer.loadNamedStyle(polygonQml)
        #self.layer_group.insertLayer(0, self.osm_diff_polygon_layer)  # now add to legend in current layer group



    def add_polygon(self, way):
        feat = QgsFeature()

        feat.setGeometry(QgsGeometry.fromWkt(way['wkt']))

        attributes = []
        attributes.append(long(way['osm_id']))
        attributes.append(way['user'])
        attributes.append(way['timestamp'])
        attributes.append(QDateTime.fromString(way['timestamp'],'yyyy-MM-ddThh:mm:ssZ').toMSecsSinceEpoch())
        # set age to 1 to always get the data visible after loading
        attributes.append(1)

        feat.setAttributes(attributes)

        self.polygon_provider.addFeatures([feat])



    def calculate_frame_age(self, layer, frame_epoch, interval):
        # set frame age for all features. Null for future features
        epoch_field_index = layer.fields().indexFromName('epoch')
        age_field_index = layer.fields().indexFromName('frame_age')
        
        for feat in layer.getFeatures():
            feat_epoch = feat.attributes()[epoch_field_index]
            if feat_epoch <= frame_epoch:
                age_msecs = frame_epoch - feat_epoch
                frame_age = ceil(age_msecs / interval)
            else:
                frame_age = None
            attrs = {age_field_index: frame_age}
            layer.dataProvider().changeAttributeValues({feat.id(): attrs})


    def update_slider(self):
        frame_epoch = ((self.dockwidget.horizontalSlider_frames.value() - 1) * self.interval_msecs) + self.animation_start_time.toMSecsSinceEpoch()
        frame_time = QDateTime.fromMSecsSinceEpoch(frame_epoch)
        self.dockwidget.label_actual_frame.setText('frame: %s (%s)' % (
            self.dockwidget.horizontalSlider_frames.value(),
            frame_time.toString(self.dockwidget.dateTimeEdit_end.displayFormat()))
        )
        #self.dockwidget.label_actual_frame.setText('frame: %s' % ())
        #self.log('update request')
        self.update_map(frame_epoch)

    def update_map(self, frame_epoch):
        if self.polygon_layer is not None:
            #self.log('updating')
            self.calculate_frame_age(self.polygon_layer, frame_epoch, self.interval_msecs)
            self.iface.mapCanvas().refreshAllLayers()
    
    def show_progress(self):
        progressMessageBar = self.iface.messageBar().createMessage("Requesting online OSM data")
        progress = QProgressBar()
        progress.setMaximum(0)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        self.iface.messageBar().pushWidget(progressMessageBar, Qgis.Info, duration=2)


    def renderLabel(self, painter):
        """Render the current timestamp on the map canvas"""
        if not self.showLabel or not self.model.hasLayers() or not self.dock.pushButtonToggleTime.isChecked():
            return

        dt = self.model.getCurrentTimePosition()
        if dt is None:
            return

        labelString = self.labelOptions.getLabel(dt)

        # Determine placement of label given cardinal directions
        flags = 0
        for direction, flag in ('N', Qt.AlignTop), ('S', Qt.AlignBottom), ('E', Qt.AlignRight), ('W', Qt.AlignLeft):
            if direction in self.labelOptions.placement:
                flags |= flag

        # Get canvas dimensions
        width = painter.device().width()
        height = painter.device().height()

        painter.setRenderHint(painter.Antialiasing, True)
        txt = QTextDocument()
        html = """<span style="background-color:%s; padding: 5px; font-size: %spx;">
                    <font face="%s" color="%s">%s</font>
                  </span> """\
               % (self.labelOptions.bgcolor, self.labelOptions.size, self.labelOptions.font,
                  self.labelOptions.color, labelString)
        txt.setHtml(html)
        layout = txt.documentLayout()
        size = layout.documentSize()

        if flags & Qt.AlignRight:
            x = width - 5 - size.width()
        elif flags & Qt.AlignLeft:
            x = 5
        else:
            x = width / 2 - size.width() / 2

        if flags & Qt.AlignBottom:
            y = height - 5 - size.height()
        elif flags & Qt.AlignTop:
            y = 5
        else:
            y = height / 2 - size.height() / 2

        painter.translate(x, y)
        layout.draw(painter, QAbstractTextDocumentLayout.PaintContext())
        painter.translate(-x, -y)  # translate back


    def export_frame(self):
        settings = QgsMapSettings()
        settings.setOutputSize(QSize(512,512))
        settings.setExtent(self.polygon_layer.extent())
        settings.setLayers([self.polygon_layer])

        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()
        img = job.renderedImage()
        img.save("/tmp/rendered2.png")


    def export_frames(self, width=1920, height=1080):

        first_frame = self.dockwidget.horizontalSlider_frames.minimum()
        last_frame = self.dockwidget.horizontalSlider_frames.maximum()
        print(u'Rendering frames: %s-%s' % (first_frame, last_frame))

        frame_width = self.dockwidget.spinBox_frame_width.value()
        frame_height = self.dockwidget.spinBox_frame_height.value()

        settings = QgsMapSettings()
        settings.setDestinationCrs(QgsCoordinateReferenceSystem(self.iface.mapCanvas().mapSettings().destinationCrs()))
        settings.setOutputSize(QSize(frame_width, frame_height))
        settings.setLayers(self.iface.mapCanvas().layers())
        settings.setExtent(self.data_zoom_extent)

        job = QgsMapRendererSequentialJob(settings)

        progress = QProgressBar()
        progress.setMaximum(last_frame)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar = self.iface.messageBar().createMessage(u'Rendering frames')
        progressMessageBar.layout().addWidget(progress)
        self.iface.messageBar().pushWidget(progressMessageBar, Qgis.Info, duration=2)

        for frame_id in range(first_frame, last_frame + 1):

            self.dockwidget.horizontalSlider_frames.setValue(frame_id)
            self.update_slider()

            job.start()
            job.waitForFinished()
            img = job.renderedImage()
            base_name = u'frame_{0}.png'.format(frame_id)
            filename = os.path.join(self.plugin_dir, u'output', base_name)
            self.log(filename)
            img.save(filename)
            progress.setValue(frame_id)
