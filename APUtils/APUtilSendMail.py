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
import email
import email.mime.application
import smtplib
from email.mime.text import MIMEText


class APSendMail (object):
"""A simple class for sending e-mails 
   without having to remember all the necessary steps.
"""
      _FromAddr   = ''
      _ToAddrs    = ''
      _CCAddrs    = ''
      _BCCAddrs   = ''
      _Body       = ''
      _Subject    = ''
      _AttachList = []
      _msg        = email.mime.Multipart.MIMEMultipart()
      def __init__(self):
          pass
      @property
      def FromAddr(self):
          return self._FromAddr
      @FromAddr.setter
      def FromAddr(self, Value):
          self._FromAddr = Value
      @property
      def ToAddrs(self):
          return self._ToAddrs
      @ToAddrs.setter
      def ToAddrs(self, Value):
          self._ToAddrs = Value
      @property
      def CCAddrs(self):
          return self._CCAddrs
      @CCAddrs.setter
      def CCAddrs(self, Value):
          self._CCAddrs = Value
      @property
      def BCCAddrs(self):
          return self._BCCAddrs
      @BCCAddrs.setter
      def BCCAddrs(self, Value):
          self._BCCAddrs = Value
      @property
      def Body(self):
          return self._Body
      @Body.setter
      def Body(self, Value):
          self._Body = Value
      @property
      def Subject(self):
          return self._Subject
      @Subject.setter
      def Subject(self, Value):
          self._Subject = Value
      def AddAttachment(self, aFileName):
          self._AttachList.append(aFileName)
      def Send_Mail(self, aMailServer):
          if self._Subject != '':
             self._msg['Subject'] = self._Subject
          if self._FromAddr != '':
             self._msg['From'] = self._FromAddr
          if self._ToAddrs != '':
             self._msg['To'] = self._ToAddrs
          if self._CCAddrs != '':
             self._msg["Cc"] = self._CCAddrs
          if self._BCCAddrs != '':
             self._msg["Bcc"] = self._BCCAddrs

          # The main body is just another attachment
          if self._Body != '':
             body = email.mime.Text.MIMEText(self._Body)
             self._msg.attach(body)

          # Add Attachments
          for aAttach in self._AttachList:
              fp=open(aAttach,'rb')
              att = email.mime.application.MIMEApplication(fp.read(), _subtype=os.path.splitext(aAttach)[1])
              fp.close()
              att.add_header('Content-Disposition', 'attachment', filename = os.path.basename(aAttach))
              self._msg.attach(att)
  
          # Send the message via our own SMTP server, but don't include the
          # envelope header. 
          s = smtplib.SMTP(aMailServer)
          # Preparing Addresses...
          all_addrs = self._ToAddrs + ", " + self._CCAddrs + ", " + self._BCCAddrs
          # DebugMode
          #s.set_debuglevel(1)
          # Send !!!
          s.sendmail(self._msg['From'], all_addrs.split(", "), self._msg.as_string())
          s.quit()  

		  
if __name__ == '__main__':
   MyMail = APSendMail()
   MyMail.FromAddr = 'test@gmail.com'
   MyMail.ToAddrs  = 'test@gmail.com'
   MyMail.CCAddrs  = 'test@gmail.com'
   #MyMail.BCCAddrs  = 'prova@pluto.com'
   MyMail.Body     = 'Messaggio di test \n'
   MyMail.Subject  = 'Messaggio di TEST - Unit Test'
   MyMail.AddAttachment(__file__)
   MyMail.Send_Mail('mail server')
