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
import exceptions

KLogDir = os.path.join(".", "logs", "")
KLogFile = KLogDir + datetime.datetime.now().strftime("%Y%m") + '.Log'

KLogParams = {'File' : {'Active' : False, 'LogFile': KLogFile, 'WriteMode': ''}, 'Console' : {'Active' : True}, 'Mail' : {'Active' : False, 'Host' : '', 'Port' : 25, 'From': '', 'To' : '', 'Subject' : '', 'User' : '', 'Password' : ''}}

def SettingLogs(aLogger, aLogParams = KLogParams):
  aLogger.setLevel(logging.DEBUG)
  # create formatter and add it to the handlers
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y%m%d %H:%M:%S')

  if aLogParams['File']['Active']:
     # create file handler which logs even debug messages
     #print aLogParams['File']['LogFile']
     if aLogParams['File']['WriteMode'] == '':
        fh = logging.FileHandler(aLogParams['File']['LogFile'])
     else:
        fh = logging.FileHandler(aLogParams['File']['LogFile'], mode=aLogParams['File']['WriteMode'])
     fh.setLevel(logging.DEBUG)
     fh.setFormatter(formatter)
     # add the handlers to the logger
     aLogger.addHandler(fh)

  if aLogParams['Console']['Active']:
     # create console handler with a higher log level
     ch = logging.StreamHandler()
     ch.setLevel(logging.DEBUG)
     ch.setFormatter(formatter)
     # add the handlers to the logger
     aLogger.addHandler(ch)

  if aLogParams['Mail']['Active']:
     mh = logging.handlers.SMTPHandler(mailhost=(aLogParams['Mail']['Host'], aLogParams['Mail']['Port']), fromaddr=aLogParams['Mail']['From'], toaddrs=aLogParams['Mail']['To'], subject=aLogParams['Mail']['Subject'], credentials=(aLogParams['Mail']['User'], aLogParams['Mail']['Password']))
     mh.setLevel(logging.DEBUG)
     mh.setFormatter(formatter)
     # add the handlers to the logger
     aLogger.addHandler(mh)
 
def GetLogger(aLoggerName, aTitle, aLogParams = KLogParams):
  # create logger 
  logger = logging.getLogger(aLoggerName) 
  SettingLogs(logger, aLogParams)
  logger.info("#"*10 + '{ ' + aTitle + ' }' + "#"*10)
  logger.info("------------------------------------------------")
  return logger 
  
# Gestione Errori
  
def extract_function_name():
    """Extracts failing function name from Traceback"""
    tb = sys.exc_info()[-1]
    stk = traceback.extract_tb(tb, 1)
    fname = stk[0][3]
    return fname
	
def log_exception(aLogger, e):
    aLogger.error("Function {function_name} raised {exception_class} ({exception_docstring}): {exception_message}".format(
    function_name = extract_function_name(), #this is optional
    exception_class = e.__class__,
    exception_docstring = e.__doc__,
    exception_message = e.message))
	
def Generate_Error_For_Tests():
    return 1/0
	
if __name__ == '__main__':
   MyLogParams = {'File' : {'Active' : False, 'LogFile': KLogFile}, 'Console' : {'Active' : True}, 'Mail' : {'Active' : False, 'Host' : '', 'Port' : 25, 'From': '', 'To' : '', 'Subject' : '', 'User' : '', 'Password' : ''}}
   aLogger = GetLogger('Test', 'Test Log', MyLogParams)
   try:
     Generate_Error_For_Tests()
   except exceptions.Exception as e:
     log_exception(aLogger, e)   
