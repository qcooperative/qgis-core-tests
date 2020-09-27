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

from qgis.utils import iface


def functionalTests():
    try:
        from qgistester.test import Test
    except:
        return []

    # advanced setting editing are reset after closing of options gui - #26327
    testAdvancedSettings = Test('Advanced settings editor saves changes')
    testAdvancedSettings.setIssueUrl('https://github.com/qgis/QGIS/issues/26327')
    testAdvancedSettings.addStep('Open QGIS Settings and change some values using Andanced Settings Editor and close dialog by pressing OK button.', prestep=lambda:_showOptions())
    testAdvancedSettings.addStep('Open QGIS Settings again. Check that previously changed settings have correct values.', prestep=lambda:_showOptions(), isVerifyStep=True)

    return [testAdvancedSettings
           ]


def _showOptions():
    iface.showOptionsDialog(None, 'mOptionsPageSettingsEditor')
