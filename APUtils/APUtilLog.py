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
# Date e Tempo
import datetime
# Gestion Log
import logging
import logging.handlers
# Gestione Errori
import traceback

KLogDir = os.path.join(".", "logs", "")
KLogFile = KLogDir + datetime.datetime.now().strftime("%Y%m") + '.Log'
KLogParams = {'LogLevel' : logging.DEBUG, 'File' : {'Active' : False, 'LogFile': KLogFile, 'WriteMode': '', 'Rotating' : {'BackupCnt': 2, 'Max': 0} }, 'Console' : {'Active' : True}, 'Mail' : {'Active' : False, 'Host' : '', 'Port' : 25, 'From': '', 'To' : '', 'Subject' : '', 'User' : '', 'Password' : ''}}

class APLogger(object):
    _LogParams = None
    _Logger = None
    def __init__(self, aLoggerName, aTitle, aLogParams = KLogParams):
          self._LogParams = aLogParams
          if self._LogParams['File']['Active']:
              self.PrepareLogPath()
          self.GetLogger(aLoggerName, aTitle)
    def PrepareLogPath(self):
        aDirName = os.sep.join(self._LogParams['File']['LogFile'].split(os.sep)[:-1])
        if (not os.path.isdir(aDirName)):
           os.makedirs(aDirName)
    #@staticmethod
    def GetLogger(self, aLoggerName, aTitle):
          # create logger
          self._Logger = logging.getLogger(aLoggerName)
          self.SettingLogs()
          self._Logger.info("#"*10 + '{ ' + aTitle + ' }' + "#"*10)
          self._Logger.info("------------------------------------------------")
          #return logger
    def SettingLogs(self):
          aLogParams = self._LogParams
          self._Logger.setLevel(aLogParams['LogLevel'])
          # create formatter and add it to the handlers
          formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y%m%d %H:%M:%S')

          if aLogParams['File']['Active']:
             # create file handler which logs even debug messages
             #print aLogParams['File']['LogFile']
             if (aLogParams['File']['Rotating']['Max'] == 0):
                 if aLogParams['File']['WriteMode'] == '':
                    fh = logging.FileHandler(aLogParams['File']['LogFile'])
                 else:
                    fh = logging.FileHandler(aLogParams['File']['LogFile'], mode=aLogParams['File']['WriteMode'])
             else:
                 if aLogParams['File']['WriteMode'] == '':
                    fh = logging.handlers.RotatingFileHandler(aLogParams['File']['LogFile'], maxBytes=aLogParams['File']['Rotating']['Max'], backupCount=aLogParams['File']['Rotating']['BackupCnt'], delay=0)
                 else:
                    fh = logging.handlers.RotatingFileHandler(aLogParams['File']['LogFile'], mode=aLogParams['File']['WriteMode'], maxBytes=aLogParams['File']['Rotating']['Max'], backupCount=aLogParams['File']['Rotating']['BackupCnt'], delay=0)
             fh.setLevel(aLogParams['LogLevel'])
             fh.setFormatter(formatter)
             # add the handlers to the logger
             self._Logger.addHandler(fh)

          if aLogParams['Console']['Active']:
             # create console handler with a higher log level
             ch = logging.StreamHandler()
             ch.setLevel(aLogParams['LogLevel'])
             ch.setFormatter(formatter)
             # add the handlers to the logger
             self._Logger.addHandler(ch)

          if aLogParams['Mail']['Active']:
             mh = logging.handlers.SMTPHandler(mailhost=(aLogParams['Mail']['Host'], aLogParams['Mail']['Port']), fromaddr=aLogParams['Mail']['From'], toaddrs=aLogParams['Mail']['To'], subject=aLogParams['Mail']['Subject'], credentials=(aLogParams['Mail']['User'], aLogParams['Mail']['Password']))
             mh.setLevel(aLogParams['LogLevel'])
             mh.setFormatter(formatter)
             # add the handlers to the logger
             self._Logger.addHandler(mh)
    # Errors Handling
    def extract_function_name(self):
            """Extracts failing function name from Traceback"""
            tb = sys.exc_info()[-1]
            stk = traceback.extract_tb(tb, 1)
            fname = stk[0][3]
            return fname
    def log_exception(self, e):
            self._Logger.error("Function {function_name} raised {exception_class} ({exception_docstring}): {exception_message}".format(
            function_name = self.extract_function_name(), #this is optional
            exception_class = e.__class__,
            exception_docstring = e.__doc__,
            exception_message = e.message))
    @property
    def Logger(self):
            return self._Logger

if __name__ == '__main__':

   def Generate_Error_For_Tests():
       return 1 / 0


   MyLogParams = {'LogLevel': logging.DEBUG, 'File': {'Active': True, 'LogFile': KLogFile, 'WriteMode': '', 'Rotating': {'BackupCnt': 2, 'Max': 50}}, 'Console': {'Active': True}, 'Mail': {'Active': False, 'Host': '', 'Port': 25, 'From':'', 'To': '', 'Subject': '', 'User': '', 'Password': ''}}
   MyLogger = APLogger('Test', 'Test Log', MyLogParams)
   aLogger = MyLogger.Logger
   try:
     Generate_Error_For_Tests()
   except Exception as e:
     MyLogger.log_exception(e)
   for I in range(1, 100):
       aLogger.info("Iteratore N.: {0}".format(I))