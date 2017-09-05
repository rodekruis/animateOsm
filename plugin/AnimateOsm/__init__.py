# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AnimateOsm
                                 A QGIS plugin
 Animates OSM changes within a time and bounding box.
                             -------------------
        begin                : 2017-09-05
        copyright            : (C) 2017 by Netherlands Red Cross
        email                : rnijssen@rodekruis.nl
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load AnimateOsm class from file AnimateOsm.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .aniosm import AnimateOsm
    return AnimateOsm(iface)
