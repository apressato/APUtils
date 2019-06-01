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


# Base
import os
import sys
import shutil
# Date e Tempo
import datetime
from datetime import date, timedelta
import time
# Vari
import hashlib
import inspect
# Filtraggio Estensioni
import fnmatch

def ForceDir(aDirPathName):
    if (not os.path.isdir(aDirPathName)):
       os.makedirs(aDirPathName)

def GetFileHash(aFileName, blocksize = 65536):
    afile = open(aFileName, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()	

def GetFileCreation(aFileName):
    return datetime.datetime.strptime(time.ctime(os.path.getctime(aFileName)), "%a %b %d %H:%M:%S %Y")
	
def GetFileLastMod(aFileName):
    return datetime.datetime.strptime(time.ctime(os.path.getmtime(aFileName)), "%a %b %d %H:%M:%S %Y")

def GetSlDirFiles(aPath, MaxLevel = None):
    slFiles = []
    num_sep = aPath.rstrip(os.path.sep).count(os.path.sep)
    for root, dirs, files in os.walk(aPath):
        # Introdotto controllo Massimo Numero di Livelli in Ricorsione Sottocartelle
        #yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if MaxLevel != None:
          if num_sep + MaxLevel <= num_sep_this:
             del dirs[:]		
        # Fine Controllo
        for currentFile in files:
            currentFile = os.path.join(root, currentFile)
            slFiles.append(currentFile)
    return slFiles

def GetSlDirFilesFiltered(aPath, Ext = '*.*', MaxLevel = None):
    slFiles = []
    slFiles = GetSlDirFiles(aPath, MaxLevel)
    if Ext != '*.*':
       tmpSlFiles = []
       tmpSlFiles = fnmatch.filter(slFiles, Ext)
       slFiles = tmpSlFiles
    return slFiles	
	
def getSlFileContent(aFileName, aClearCRLF = None):
    if aClearCRLF == True:
       slResult = [line.replace('\n', '') for line in (open(aFileName, 'rt'))]
    else:
       slResult = [line for line in (open(aFileName, 'rt'))]
    return slResult

def Appendi_Str_To_File(aFileName, aStr):
   f = open(aFileName, 'a') 
   f.write(aStr)
   f.close
   
def Scrivi_Str_To_File(aFileName, aStr):
   f = open(aFileName, 'w') 
   f.write(aStr)
   f.close
	
def Scrivi_To_File(aFileName, aStr, aAppend = 'None'):
    if aAppend:
       Appendi_Str_To_File(aFileName, aStr)
    else:
       Scrivi_Str_To_File(aFileName, aStr)

def ExtractFileName(aFilePath):
    sResult = aFilePath.split(os.sep)[-1]
    return sResult 
   
def ExtractFilePath(aFileName):
    sResult = os.sep.join(aFileName.split(os.sep)[:-1])
    return sResult
	
def ExtractFileExt(aFileName):
    sResult = '.' + aFileName.split('.')[-1]
    return sResult
	
def ChangeFileExt(aFileName, aNewExtension):
    if aNewExtension != None:
       NewExt = aNewExtension if aNewExtension[0] == '.' else '.' + aNewExtension
    sResult = os.path.splitext(aFileName)[0] + NewExt
    return sResult
	
def ChangeFilePath(aFileName, aNewPath):
    NewPath = aNewPath if aNewPath[-1] != ':' else aNewPath + os.sep # Only for Windows
    sResult = os.path.join(NewPath, aFileName.split(os.sep)[-1])
    return sResult
	
def BackupFile(aFileName, aBckPath = None, aAddDate = False, aDedupSuffix = '(#)'):
    CurrentPath = ExtractFilePath(aFileName)
    CurrentFileName = ExtractFileName(aFileName)
    CurrentExt = ExtractFileExt(CurrentFileName)
    NewSuffix = ''
    NewDedupSuffix = ''
    # Calcolo Nuovo Percorso
    if aBckPath == None:
       NewPath = CurrentPath
    else:
       NewPath = aBckPath
    # Calcolo suffisso data
    if aAddDate == True:
       NewSuffix = '-' + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Verifico se devo Deduplicare
    NewFileName = os.path.join(NewPath, "{0}{1}".format(CurrentFileName, NewSuffix))
    DedupCounter = 0
    while os.path.exists(NewFileName + CurrentExt):
      DedupCounter = DedupCounter + 1
      NewDedupSuffix = '_' + aDedupSuffix.split('#')[0] + str(DedupCounter) + aDedupSuffix.split('#')[-1]
    if NewDedupSuffix != '':
       NewFileName = NewFileName + NewDedupSuffix
    # Assemblo le ultime parti del nome ...
    NewFileName = NewFileName +	CurrentExt
    # e rinomino / sposto il file
    shutil.move(aFileName, NewFileName)	
	
def SplitFileName(aFileName):
    Path = os.sep.join(aFileName.split(os.sep)[:-1])
    FileName = aFileName.split(os.sep)[-1].split(".")[0]
    Ext = '.' + aFileName.split('.')[-1]
    return Path, FileName, Ext
	
def GetCurrentScriptSplit():
    CurrentScript = inspect.getfile(inspect.currentframe()) # script filename (usually with path)
    CurrentPath, CurrentFile, CurrentExt = SplitFileName(CurrentScript)
    return CurrentPath, CurrentFile
	
if __name__ == '__main__':
    MyslFiles = GetSlDirFiles('.')
    for myfile in MyslFiles:
       print ("File: {0} || Hash: {1} || DtCreate: {2} || DTMod: {3} \n".format(myfile, GetFileHash(str(myfile)), GetFileCreation(myfile), GetFileLastMod(myfile)))
    
    MyTxt = getSlFileContent(__file__, True)
    for line in MyTxt:
      print (line)
    #Appendi_Str_To_File(os.path.join('.', 'TestAppend.txt'), '\n'.join(MyTxt))
    print (ExtractFileName(os.path.join(".", __file__)))
    print (ExtractFilePath(os.path.join(".", __file__)))
    print (ExtractFileExt(os.path.join(".", __file__)))
    print (ChangeFileExt(os.path.join(".", __file__), 'ini'))
    print (ChangeFilePath(os.path.join(".", __file__), 'C:'))