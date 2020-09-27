# -*- coding: utf-8 -*-

"""
***************************************************************************
    coretestsplugin.py
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


class CoreTestsPlugin:

    def __init__(self, iface):
        self.iface = iface

        try:
            from coretests.tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, 'Core Tests')
        except Exception as e:
            raise
            pass

    def initGui(self):
        pass

    def unload(self):
        try:
            from coretests.tests import testerplugin
            from qgistester.tests import removeTestModule
            removeTestModule(testerplugin, 'Core Tests')
        except:
            pass
