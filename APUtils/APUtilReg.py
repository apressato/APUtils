#   This file is part of APUtils.
#   APUtils is a porting with addictions of some Embarcadero Delphi VCL Functions
#   made by APressato <apressato@gmail.com> in 2018 - 2019.
#
#   APUtils is free software: you can redistribute it and/or modify
#   it under the terms of the
#   Creative Commons Attribution ShareAlike 4.0 International
#   as published by Creative Commons.
#
#   APUtils is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   Creative Commons Attribution ShareAlike 4.0 International for more details.
#
#   You should have received a copy of the
#   Creative Commons Attribution ShareAlike 4.0 International
#   along with APUtils. If not,
#   see <https://creativecommons.org/licenses/by-sa/4.0/legalcode>.

import os
import winreg
import platform

class APReg(object):
    __default_Architecture_Key = {0}  #System default
    __Root_Key = -1
    def __is_os_64bit():
        return platform.machine().endswith('64')

    def __init__(self):
        pass

    def KeyExists(self, aKey):
        exists = True
        try:
            TestKey = winreg.OpenKey(self.__Root_Key, aKey, 0, winreg.KEY_WRITE | self.__default_Architecture_Key)
            winreg.CloseKey(TestKey)
        except WindowsError:
            exists = False
        return exists

    def DeleteKey(self, aKey):
        bResult = False
        if self.KeyExists(aKey):
           bResult = winreg.DeleteKeyEx(self.__Root_Key, aKey, self.__default_Architecture_Key)
        return bResult

    def DeleteValue(self, aKey, aValue):
        bResult = False
        try:
            TestKey = winreg.OpenKey(self.__Root_Key, aKey, 0, winreg.KEY_WRITE | self.__default_Architecture_Key)
