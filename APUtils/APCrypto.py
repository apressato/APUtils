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

import base64
import sys


class APCryptoSuite(object):
    _FOffSet = []
    _RandomPhrase = ''
    _KOffSetArray = []

    def _GetOffSet(self, aPos, OffArray):
        Result = OffArray[-1]
        if (aPos % len(OffArray)) > 0:
            Result = OffArray[aPos % len(OffArray)]
        return Result

    def _Crypt(self, St, OffArray):
        Result = ''
        for I in range(len(St)):
            # Result = Result + chr((ord(St[I]) - len(St) - I - self._GetOffSet(I, OffArray))%256)
            Result = Result + chr(self.GetOverflowed(ord(St[I]) - len(St) - I - self._GetOffSet(I, OffArray)))
        return Result

    def _Decrypt(self, St, OffArray):
        Result = ''
        for I in range(len(St)):
            # Result = Result + chr((ord(St[I]) + len(St) + I + self._GetOffSet(I, OffArray))%256)
            Result = Result + chr(self.GetOverflowed(ord(St[I]) + len(St) + I + self._GetOffSet(I, OffArray)))
        return Result

    def _EncodeMime(self, St):
        Result = ""
        if self.GetPythonVer() == 3:
            Result = base64.b64encode(St.encode('utf-8'))
        elif self.GetPythonVer() < 3:
            Result = base64.b64encode(St)
        return Result

    def _DecodeMime(self, St):
        Result = ""
        if self.GetPythonVer() == 3:
            Result = base64.b64decode(St).decode('utf-8')
        elif self.GetPythonVer() < 3:
            Result = base64.b64decode(St)
        return Result

    def _OffSetStrFromPhrase(self, St):
        self._FOffSet = []
        for token in St.split():
            self._FOffSet.append(ord(token[0]))

    def _PrepareOffSet(self):
        if self.RandomPhrase is None:
            self._FOffSet = self._KOffSetArray
        else:
            self._OffSetStrFromPhrase(self.RandomPhrase)

    def __init__(self):
        self._KOffSetArray = [7, 4, 5, 6]

    def Encrypt(self, St):
        self._PrepareOffSet()
        Result = self._EncodeMime(self._Crypt(St, self._FOffSet)).decode('utf-8')
        return Result

    def Decrypt(self, St):
        self._PrepareOffSet()
        Result = self._Decrypt(self._DecodeMime(St), self._FOffSet)
        return Result

    def GetOverflowed(self, aValue):
        result = aValue
        if aValue > 256:
            result = aValue % 256
        elif aValue < 0:
            result = (aValue % 256)
        return result

    def GetPythonVer(self):
        return sys.version_info[0]

    @property
    def RandomPhrase(self):
        return self._RandomPhrase

    @RandomPhrase.setter
    def RandomPhrase(self, value):
        self._RandomPhrase = value


def APEncryptPassword(aRandomPhrase, aPassword):
    MyAPCryptoSuite = APCryptoSuite()
    MyAPCryptoSuite.RandomPhrase = aRandomPhrase
    Result = MyAPCryptoSuite.Encrypt(aPassword)
    return Result


def APDecryptPassword(aRandomPhrase, aPassword):
    MyAPCryptoSuite = APCryptoSuite()
    MyAPCryptoSuite.RandomPhrase = aRandomPhrase
    Result = MyAPCryptoSuite.Decrypt(aPassword)
    return Result


if __name__ == '__main__':
    SecretPhrase = "Python Is Awesome !!!"
    # SecretPhrase = None
    enc_result = APEncryptPassword(SecretPhrase, 'P4ssw0rd')
    print(enc_result)
    dec_result = APDecryptPassword(SecretPhrase, enc_result)
    print(dec_result)
