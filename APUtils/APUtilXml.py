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


KHTMLType = 0
KXMLType  = 1

KEscapeSeqHTML = [('&', '&amp;'),
                  ('<', '&lt;'),
                  ('>', '&gt;'),
                  ('"', '&quot;'),
                  ('\'', '&apos;'),
                  (chr(224), '&agrave;'),
                  (chr(225), '&aacute;'),
                  (chr(232), '&egrave;'),
                  (chr(233), '&eacute;'),
                  (chr(236), '&igrave;'),
                  (chr(237), '&iacute;'),
                  (chr(242), '&ograve;'),
                  (chr(243), '&oacute;'),
                  (chr(249), '&ugrave;'),
                  (chr(250), '&uacute;')]
				  
				  
KEscapeSeqXML = [('&', '&amp;'),
                 ('<', '&lt;'),
                 ('>', '&gt;'),
                 ('"', '&quot;'),
                 ('\'', '&apos;')]
			  
def GetEscapedText(aText, aEscapeType = KXMLType):
    """Escapes invalid XML characters."""
    EscapeSeq = []
    if aEscapeType == KHTMLType:
       EscapeSeq = KEscapeSeqHTML
    else:
       EscapeSeq = KEscapeSeqXML
    for Seq in EscapeSeq:
        aText = aText.replace(Seq[0], Seq[1])
    return aText

 	
	
 	
 	
 	
 	
 	
 	
 	
 	
