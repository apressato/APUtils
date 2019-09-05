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

tmttPlainText = 0
tmttHtml = 1
tMailTextType = {tmttPlainText, tmttHtml}


class APSendMail(object):
    """A simple class for sending e-mails
         without having to remember all the necessary steps.
         Simply set property and send the message
         :Param FromAddr:
            Sender Address
         :Param ToAddrs:
            Receiver Address List separated by ", "
         :Param CCAddrs:
            Carbon Copy Receiver Address List separated by ", "
         :Param BCCAddrs:
            Blind Carbon Copy Receiver Address List separated by ", "
         :Param Boby:
            The Body of the message (in Plain Text)
         :Param Subject:
            The Subject of the message

         :Param MailTextType:
         :Param AuthUser:
         :Param AuthPassword:
         :Param UseTls:

AddAttachment(self, aFileName):
Send_Mail(self, aMailServer, aServerPort=None, ShowServerResponse=False):

      """
    _FromAddr = ''
    _ToAddrs = ''
    _CCAddrs = ''
    _BCCAddrs = ''
    _Body = ''
    _Subject = ''
    _MailTextType = tmttPlainText
    _AttachList = []
    _AuthUser = None
    _AuthPassword = None
    _UseTls = False
    _msg = email.mime.Multipart.MIMEMultipart()

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

    @property
    def MailTextType(self):
        return self._MailTextType

    @MailTextType.setter
    def MailTextType(self, Value):
        if Value in tMailTextType:
            self._MailTextType = Value
        else:
            raise ValueError('Admitted Text Types are {0}, current {1}.'.format(self._MailTextType, Value))

    @property
    def AuthUser(self):
        return self._AuthUser

    @AuthUser.setter
    def AuthUser(self, Value):
        self._AuthUser = Value

    @property
    def AuthPassword(self):
        return self._AuthPassword

    @AuthPassword.setter
    def AuthPassword(self, Value):
        self._AuthPassword = Value

    @property
    def UseTls(self):
        return self._UseTls

    @UseTls.setter
    def UseTls(self, Value):
        self._UseTls = Value

    def AddAttachment(self, aFileName):
        self._AttachList.append(aFileName)

    def Send_Mail(self, aMailServer, aServerPort=None, ShowServerResponse=False):
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
            if self._MailTextType == tmttPlainText:
                body = email.mime.Text.MIMEText(self._Body, 'plain')
            elif self._MailTextType == tmttHtml:
                body = email.mime.Text.MIMEText(self._Body, 'html')
        self._msg.attach(body)

        # Add Attachments
        for aAttach in self._AttachList:
            fp = open(aAttach, 'rb')
            att = email.mime.application.MIMEApplication(fp.read(), _subtype=os.path.splitext(aAttach)[1])
            fp.close()
            att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(aAttach))
            self._msg.attach(att)

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        if aServerPort is not None:
            Server = smtplib.SMTP(aMailServer, aServerPort)
        else:
            Server = smtplib.SMTP(aMailServer)

        # DebugMode
        if ShowServerResponse:
            Server.set_debuglevel(1)

        # Encrypted SMTP
        if self._UseTls:
            Server.starttls()

        # Authentication
        if self._AuthPassword is not None:
            if self._AuthUser is None:
                self._AuthUser = self._FromAddr
            Server.login(self._AuthUser, self._AuthPassword)

        # Preparing Addresses...
        all_addrs = self._ToAddrs + ", " + self._CCAddrs + ", " + self._BCCAddrs

        # Send !!!
        Server.sendmail(self._msg['From'], all_addrs.split(", "), self._msg.as_string())
        Server.quit()


if __name__ == '__main__':
       MyMail = APSendMail()
       MyMail.FromAddr = 'test@gmail.com'
       MyMail.ToAddrs  = 'test1@gmail.com'
       MyMail.CCAddrs  = 'test2@gmail.com'
       MyMail.BCCAddrs  = 'prova@pluto.com'
       MyMail.Body     = 'Messaggio di test \n'
       MyMail.Subject  = 'Messaggio di TEST - Unit Test'
       MyMail.AddAttachment(__file__)
       MyMail.AuthUser = "YourAccount@gmail.com"
       MyMail.AuthPassword = "Your Password for Apps"
       MyMail.UseTls = True
       MyMail.Send_Mail('smtp.gmail.com', 587, True)
