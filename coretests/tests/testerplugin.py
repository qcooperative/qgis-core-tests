# -*- coding: utf-8 -*-

"""
***************************************************************************
    testerplugin.py
    ---------------------
    Date                 : May 2016
    Copyright            : (C) 2016 by Boundless, http://boundlessgeo.com
                         : (C) 2020 by QCooperative, https://www.qcooperative.net
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'May 2016'
__copyright__ = '(C) 2016 Boundless, http://boundlessgeo.com'

import os
import sys

from qgis.core import QgsSettings, QgsApplication, QgsProject
from qgis.utils import iface

from processing.gui.BatchAlgorithmDialog import BatchAlgorithmDialog

pluginPath = os.path.split(os.path.dirname(__file__))[0]
dataPath = os.path.join(pluginPath, 'data')


def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    # advanced setting editing are reset after closing of options gui - #26327
    testAdvancedSettings = Test('Advanced settings editor saves changes')
    testAdvancedSettings.setIssueUrl('https://github.com/qgis/QGIS/issues/26327')
    testAdvancedSettings.addStep('Open QGIS Settings and change some values using Advanced Settings Editor and close dialog by pressing OK button.', prestep=lambda:_showOptions(), busyCursor=False)
    testAdvancedSettings.addStep('Open QGIS Settings again. Check that previously changed settings have correct values.', prestep=lambda:_showOptions(), isVerifyStep=True, busyCursor=False)

    # adding WMTS from Browser paner - #36264
    testBrowserAddWmts = Test('Adding WMTS from Browser')
    testBrowserAddWmts.setIssueUrl('https://github.com/qgis/QGIS/issues/36264')
    testBrowserAddWmts.addStep('Create test WMTS connection.', function=lambda: _addWmtsConnection())
    testBrowserAddWmts.addStep('Expand "WMS/WMTS" node in the Browser panel. Then expand "TesterPlugin" connection.')
    testBrowserAddWmts.addStep('Try to add layer "112 Par satellite" from the Browser to QGIS canvas. Check that QGIS prompts for date and after setting a date layer added to canvas and visible.', isVerifyStep=True)
    testBrowserAddWmts.setCleanup(lambda: _removeWmtsConnection())

    # adding rows in the Processing batch interface - #39696
    testAddBatchRows = Test('Adding new rows in Processing batch interface')
    testAddBatchRows.setIssueUrl('https://github.com/qgis/QGIS/issues/39696')
    testAddBatchRows.addStep('Start native "Buffer" algorithm in batch mode', function=lambda: _runProcessingBatch(), busyCursor=False)
    testAddBatchRows.addStep('Check that every time green plus button in the dialog toolbar is pressed a new row added to the batch.', isVerifyStep=True)
    testAddBatchRows.addStep('Close dialog by pressing "Close" button.')

    # filename prefix not shown when loading GPX or similar files - #37551
    testGpxFilenamePrefix = Test('Filename prefix is not shown when adding layers from GPX')
    testGpxFilenamePrefix.setIssueUrl('https://github.com/qgis/QGIS/issues/37551')
    testGpxFilenamePrefix.addStep('Add GPX layer to QGIS. Ensure that all layers in the "Select Vector Layers to Add" dialog are selected and "Add layers to group" checkbox is checked. Press "OK" button', prestep=lambda: iface.addVectorLayer(os.path.join(dataPath, 'elev.gpx'),'elev','ogr'), busyCursor=False)
    testGpxFilenamePrefix.addStep('Check that in the layer tree there is an "elev" group with 5 layers inside it and layer names are not prefixed with the "elev".', isVerifyStep=True)
    testGpxFilenamePrefix.addStep('Remove group with layers from the project.', function=lambda: QgsProject.instance().clear())
    testGpxFilenamePrefix.addStep('Add GPX layer to QGIS. Ensure that all layers in the "Select Vector Layers to Add" dialog are selected and "Add layers to group" checkbox is NOT checked. Press "OK" button', prestep=lambda: iface.addVectorLayer(os.path.join(dataPath, 'elev.gpx'),'elev','ogr'), busyCursor=False)
    testGpxFilenamePrefix.addStep('Check that in the layer tree there are 5 layers and their layer names are prefixed with the "elev".', isVerifyStep=True)
    testGpxFilenamePrefix.setCleanup(lambda: QgsProject.instance().clear())

    # check Processing providers
    testProcessingProviders = Test('Processing providers are functional')
    testProcessingProviders.addStep('Open Processing toolbox from the "Processing -> Toolbox" menu')
    testProcessingProviders.addStep('Verify that native QGIS tools groups are exist in the Processing toolbox.', isVerifyStep=True)
    testProcessingProviders.addStep('Verify that the GDAL group is exist in the Processing toolbox and that it contains several sub-groups.', isVerifyStep=True)
    testProcessingProviders.addStep('Verify that the GRASS group is exist in the Processing toolbox and that it contains several sub-groups.', isVerifyStep=True)
    testProcessingProviders.addStep('Verify that the SAGA group is exist in the Processing toolbox and that it contains several sub-groups.', isVerifyStep=True)

    return [testAdvancedSettings,
            testBrowserAddWmts,
            testAddBatchRows,
            testGpxFilenamePrefix,

            # generic tests not linked to any ticket
            testProcessingProviders
           ]


def _showOptions():
    iface.showOptionsDialog(None, 'mOptionsPageSettingsEditor')


def _addWmtsConnection():
    settings = QgsSettings()
    key = 'qgis/connections-wms/TesterPlugin'

    settings.setValue(key + '/url', 'http://wmts.geo.admin.ch/1.0.0/WMTSCapabilities.xml?lang=fr')
    settings.setValue(key + '/dpiMode', 7)
    settings.setValue(key + '/ignoreAxisOrientation', False)
    settings.setValue(key + '/ignoreGetFeatureInfoURI', False)
    settings.setValue(key + '/ignoreGetMapURI', False)
    settings.setValue(key + '/ignoreReportedLayerExtents', False)
    settings.setValue(key + '/invertAxisOrientation', False)
    settings.setValue(key + '/referer', '')
    settings.setValue(key + '/smoothPixmapTransform', False)

    iface.browserModel().reload()


def _removeWmtsConnection():
  settings = QgsSettings()
  settings.remove('qgis/connections-wms/TesterPlugin')
  settings.remove('qgis/WMS/TesterPlugin')
  iface.browserModel().reload()


def _runProcessingBatch():
    alg = QgsApplication.processingRegistry().createAlgorithmById('native:buffer')
    dlg = BatchAlgorithmDialog(alg.create(), parent=iface.mainWindow())
    dlg.show()
    dlg.exec_()
