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

import ast

ptLeft = 0
ptRight = 1
ptCenter = 2

def StringToStructure(aStr):
    """Transform a string into a python structure.
       Example:
       "{test: 1}" -> {test: 1}
    """
    return ast.literal_eval(aStr)

def CapitalizeToken(aToken):
    sResult = ''
    if len(aToken) > 0:
        sResult = str(aToken[0]).upper() + aToken[1:]
    return sResult

def Capitalize(aStr, RespectCase = False):
    sResult = aStr
    if RespectCase:
       MyStr = [(CapitalizeToken(txt)) for txt in aStr.split(' ')]
       sResult = ' '.join(MyStr)
    else:
       sResult = aStr.capitalize()
    return sResult

def APPad(aStr, PaddingChar, PaddingLenght, PaddingType = ptLeft):
    sResult = aStr
    if PaddingType == ptLeft:
       sResult = aStr.ljust(PaddingLenght, PaddingChar)
    elif PaddingType == ptRight:
       sResult = aStr.rjust(PaddingLenght, PaddingChar)
    elif PaddingType == ptCenter:
       PerSide = (PaddingLenght - len(aStr)) // 2
       sResult = aStr.rjust(len(aStr) + PerSide, PaddingChar)
       sResult = sResult.ljust(PaddingLenght, PaddingChar)
    return sResult	   

def APPadClipper(aStr, PaddingChar, PaddingLenght, PaddingType = ptLeft, TruncToLen = True):
    sResult = APPad(aStr, PaddingChar, PaddingLenght, PaddingType)
    if TruncToLen:
       return sResult[:PaddingLenght]
    else:
       return sResult

def SortString(aStr):
    return ''.join(sorted(aStr))

def DelChar(aStr, aChr):
    sResult = aStr
    if aStr != '':
       sResult = ''
       for ch in aStr:
          if ch != aChr:
            sResult += ch
    return sResult

def DelAllChar(aStr, aDelChrs):
    sResult = aStr
    for ch in aDelChrs:
       sResult = DelChar(sResult, ch)
    return sResult

def TrimRightChar (aStr, Ch):
    sResult = aStr
    if aStr != '':
       while (len(sResult)>0) and (sResult[-1] == Ch):
            sResult = sResult[:-1]
    return sResult	

def TrimLeftChar (aStr, Ch):
    sResult = aStr
    if aStr != '':
       while (len(sResult)>0) and (sResult[0] == Ch):
            sResult = sResult[1:]
    return sResult	

def TrimRightLeftChar (aStr, Ch):
    sResult = aStr
    if aStr != '':
       sResult = TrimRightChar(aStr, Ch)
       sResult = TrimLeftChar(sResult, Ch)
    return sResult

def ReduceCommonFactorChar(aStr, Ch):
   sResult = aStr
   if aStr != '':
      while sResult.find(Ch + Ch) > -1:
           sResult = sResult.replace(Ch + Ch, Ch)
   return sResult
   
def ReduceCommonFactorSpaces(aStr):
   return ReduceCommonFactorChar(aStr, ' ')
   
def TrimFuzzies(aStr):
   NonFuzzies = "' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
   sResult = aStr
   if aStr != '':
     sResult = ''
     for ch in aStr:
        if ch in NonFuzzies:
          sResult += ch
     sResult = ReduceCommonFactorSpaces(sResult)
     sResult = sResult.strip()
   return sResult	 

def ReplaceAllChars(aStr, OldChars, NewChars, RaiseErrors = False):
   sResult = aStr
   if len(OldChars) != len(NewChars):
      if RaiseErrors:
         raise ValueError("OldChars and NewChars must have the same lenght")
      else:
         return sResult
   for i in range(len(OldChars)):
      sResult = sResult.replace(OldChars[i], NewChars[i])
   return sResult
   

if __name__ == "__main__":
    print(StringToStructure('{"Nikhil" : 1, "Akshat" : 2, "Akash" : 3}'))
    print(Capitalize('Python is Awesome'))
    print(Capitalize('Python is AWesome', True))
    print(APPad(' Left Pad ', '=', 20))
    print(APPad(' Right Pad ', '=', 20, ptRight))
    print(APPad(' Center Pad ', '=', 20, ptCenter))
    print(APPadClipper(' Left Pad ', '=', 8))
    print(APPadClipper(' Right Pad ', '=', 8, ptRight))
    print(APPadClipper(' Center Pad ', '=', 8, ptCenter))
    print(SortString('425361'))
    print(DelChar('11123111451116111', '1'))
    print(DelAllChar('1234567890', '13579'))
    print(TrimRightChar('1234567890---------------', '-'))
    print(TrimLeftChar('------1234567890', '-'))
    print(TrimRightLeftChar('------------1234567890----------', '-'))
    print(ReduceCommonFactorChar('12--34--56--78---90-', '-'))
    print(ReduceCommonFactorSpaces('Python     is      Awesome'))
    print(TrimFuzzies('Python### is @@@@@@@Awesome'))
    print(ReplaceAllChars('We#Are-Legion', '#-', '  ', True))
