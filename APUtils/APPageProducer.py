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

import re

class APPageProducer (object):
    _Source = ''
    _Response = ''
    _SearchPattrern = '<\s*#[^>]*\s*(\w\d\=)*>'
    _ExtractNamePattern = '\w[^><#]*'
    def get_CleanedTag(self, aTag):
        return re.search(self._ExtractNamePattern, aTag.replace('\n', ' ')).group()
    def __init__(self):
        pass
    def Internal_Parser(self):
        AttributeDict = {}
        _ReplaceTxt = ''
        for x in re.finditer(self._SearchPattrern, self._Source, re.I|re.M):
            TagInfoStr = x.group(0)
            TagInfoStrCln = self.get_CleanedTag(x.group(0))
            TagInfoList = TagInfoStrCln.split(' ')
            if len(TagInfoList) > 1:
                for Attribute in TagInfoList[1:]:
                    AttValue = str(Attribute).split('=')
                    AttributeDict[AttValue[0]] = AttValue[-1].replace('"', '')
                _ReplaceTxt = self.PageProducerTag(TagInfoList[0], AttributeDict)
            else:
                _ReplaceTxt = self.PageProducerTag(TagInfoList[0], None)

            if _ReplaceTxt != None:
                self._Response = self._Response.replace(TagInfoStr, _ReplaceTxt)
    def rebuildAttributes(self, TagAttributes):
        sResult = ''
        for Tag in TagAttributes:
            sResult = sResult + " " + "{0}={1}".format(Tag, TagAttributes[Tag])
        return sResult.strip()
    def rebuildTag(self, TagString, TagAttributes):
        if TagAttributes != None:
            sResult = "<#{0} {1}>".format(TagString, self.rebuildAttributes(TagAttributes))
        else:
            sResult = "<#{0}>".format(TagString)
        return sResult
    def response(self, aText):
        self._Source = aText
        self._Response = aText
        self.Internal_Parser()
        return self._Response
    def PageProducerTag(self, TagString, TagAttributes):
        pass


class TestClass (APPageProducer):
    def PageProducerTag(self, TagString, TagAttributes):
        sResult = None
        print(TagString)
        if TagAttributes != None:
            print(TagAttributes)
        if TagString == 'appname':
            sResult = 'APressato Page Producer Class'
        return sResult

if __name__ == '__main__':
    TestStr = '''<html>
<head>
<title>Producer Demo</title>
</head>
<body>
<h1>Producer Demo</h1>
<p>This is a demo of the page produced by the <b><#appname></b> application on
<b><#date></b>.</p>
<hr>
<p>The prices in this catalog are valid until <b><#expiration
days=21 type=3></b>.</p>
<#Pippo>
</body>
</html>'''

    MyClass = TestClass()
    print(MyClass.response(TestStr))