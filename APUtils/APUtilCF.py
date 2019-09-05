# -*- coding: utf-8 -*-

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

import datetime

array_Dispari = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]
Mesi           = "ABCDEHLMPRST"

class CodiceFiscale(object):
  _Nome            = ''
  _Cognome         = ''
  _Sesso           = ''
  _DataNascita     = None
  _BelfioreNascita = ''
  def __init__(self):
      pass
  def __normalizza(self, aStr):
      sResult = ''
      for ch in aStr.lower():
          if (ch == 'è') or (ch == 'é'): 
             sResult = sResult + 'e'
          elif ch == 'à':
             sResult = sResult + 'a'
          elif ch == 'ù':
             sResult = sResult + 'u'
          elif ch == 'ò':
             sResult = sResult + 'o'
          elif ch == 'ì':
             sResult = sResult + 'i'
          else:
            sResult = sResult + ch
      return sResult.upper()
  def __conta_voc(self, aStr):
      nResult = 0
      for ch in aStr:
        if ch in ['A', 'E', 'I', 'O', 'U']:
           nResult = nResult + 1
      return nResult
  def __conta_cons(self, aStr):
      nResult = 0
      for ch in aStr:
        if ch not in ['A', 'E', 'I', 'O', 'U']:
           nResult = nResult + 1
      return nResult
  def __voc_num(self, aStr, aPos):
      sResult = '@'
      num = 0
      for ch in aStr:
        if ch in ['A', 'E', 'I', 'O', 'U']:
           num = num + 1
           if num == aPos:
              sResult = ch
              break
      return sResult
  def __cons_num(self, aStr, aPos):
      sResult = '@'
      num = 0
      for ch in aStr:
        if ch not in ['A', 'E', 'I', 'O', 'U']:
           num = num + 1
           if num == aPos:
              sResult = ch
              break
      return sResult
  def __getcogn3char(self, cognome):
      sResult = ''
      aStr = self.__normalizza(cognome)
      nvoc = self.__conta_voc(aStr)
      ncons = self.__conta_cons(aStr)
      if ncons >= 3:
         sResult = self.__cons_num(aStr, 1) + self.__cons_num(aStr, 2) + self.__cons_num(aStr, 3)
      elif ncons == 2:
         sResult = self.__cons_num(aStr, 1) + self.__cons_num(aStr, 2) + self.__voc_num(aStr, 1) 
      elif (ncons == 1) and (nvoc >= 2):
         sResult = self.__cons_num(aStr, 1) + self.__voc_num(aStr, 1) + self.__voc_num(aStr, 2)		 
      elif (ncons == 1) and (nvoc == 1):
         sResult = self.__cons_num(aStr, 1) + self.__voc_num(aStr, 1) + 'X'		 
      elif (nvoc == 2):
         sResult = self.__voc_num(aStr, 1) + self.__voc_num(aStr, 2) + 'X'	 
      else:
         sResult = ''
      return sResult
  def __getnome3char(self, nome):
      sResult = ''
      aStr = self.__normalizza(nome)
      nvoc = self.__conta_voc(aStr)
      ncons = self.__conta_cons(aStr)
      if ncons >= 4:
         sResult = self.__cons_num(aStr, 1) + self.__cons_num(aStr, 3) + self.__cons_num(aStr, 4)
      elif ncons == 3:
         sResult = self.__cons_num(aStr, 1) + self.__cons_num(aStr, 2) + self.__cons_num(aStr, 3) 
      elif ncons == 2:
         sResult = self.__cons_num(aStr, 1) + self.__cons_num(aStr, 2) + self.__voc_num(aStr, 1) 
      elif (ncons == 1) and (nvoc >= 2):
         sResult = self.__cons_num(aStr, 1) + self.__voc_num(aStr, 1) + self.__voc_num(aStr, 2)		 
      elif (ncons == 1) and (nvoc == 1):
         sResult = self.__cons_num(aStr, 1) + self.__voc_num(aStr, 1) + 'X'		 
      elif (nvoc == 2):
         sResult = self.__voc_num(aStr, 1) + self.__voc_num(aStr, 2) + 'X'	 
      else:
         sResult = ''
      return sResult
  def __get_mese_ch(self, aMeseNum):
      return Mesi[aMeseNum - 1]
  def __DataNa2DataCF(self, aDataNa, aSesso):
      # t = datetime.datetime.strptime(aDataNa, '%d/%m/%Y')
      t = aDataNa
      Offset = 40 if aSesso in "fF" else 0
      return "{:>02}{}{:>02}".format(t.year % 100, self.__get_mese_ch(t.month), t.day + Offset)
  def __Cod_Pari(self, aCh):
      return ord(aCh) - (ord('0') if aCh.isdigit() else ord('A'))
  def __Cod_Dispari(self, aCh):
      return array_Dispari[ord(aCh) - (ord('0') if aCh.isdigit() else ord('A'))]
  def __get_CodiceControllo(self, aCF):
      SommaDispari = sum(self.__Cod_Dispari(x) for x in aCF[::2])
      SommaPari    = sum(self.__Cod_Pari(x) for x in aCF[1::2])
      return chr(ord('A') + ((SommaDispari + SommaPari) % 26))
  def get_codice_fiscale(self):
      cfBase = "{}{}{}{}".format(self.__getcogn3char(self._Cognome), self.__getnome3char(self._Nome), self.__DataNa2DataCF(self._DataNascita, self._Sesso), self._BelfioreNascita)
      return "".join([cfBase, self.__get_CodiceControllo(cfBase)])
  def check_CodiceControllo(self, aCF):
      internalCF = aCF.upper()
      return self.__get_CodiceControllo(internalCF[:15]) == internalCF[15]
  def Calcola_Compara(self, aCFToCompare):
      internalCF = self.get_codice_fiscale()
      return internalCF == aCFToCompare
  @property
  def Nome(self):
      return self._Nome
  @Nome.setter
  def Nome(self, Value):
      self._Nome = Value
  @property
  def Cognome(self):
      return self._Cognome
  @Cognome.setter
  def Cognome(self, Value):
      self._Cognome = Value
  @property
  def Sesso(self):
      return self._Sesso
  @Sesso.setter
  def Sesso(self, Value):
      self._Sesso = Value
  @property
  def DataNascita(self):
      return self._DataNascita
  @DataNascita.setter
  def DataNascita(self, Value):
      self._DataNascita = Value
  @property
  def BelfioreNascita(self):
      return self._BelfioreNascita
  @BelfioreNascita.setter
  def BelfioreNascita(self, Value):
      self._BelfioreNascita = Value


if __name__ == "__main__":
   CalcCF = CodiceFiscale()
   CalcCF.Nome    = "Maria"
   CalcCF.Cognome = "Rossi"
   CalcCF.Sesso   = "F"
   CalcCF.BelfioreNascita = "F205"
   CalcCF.DataNascita = datetime.datetime.strptime("15/08/1974", "%d/%m/%Y")
   print ("Car{} {} {}, il tuo codice fiscale e': {}".format("o" if CalcCF.Sesso in 'mM' else "a", CalcCF.Nome, CalcCF.Cognome, CalcCF.get_codice_fiscale()))
   print ("Eseguo una verifica sul codice di controllo per RSSMRA74M55F205K: {}".format("Corretto!" if CalcCF.check_CodiceControllo('RSSMRA74M55F205K') else "ERRATO!!!"))
   print ("Eseguo una verifica sul codice di controllo per RSSMRA74M55F205I: {}".format("Corretto!" if CalcCF.check_CodiceControllo('RSSMRA74M55F205I') else "ERRATO!!!"))
   print ("Eseguo una verifica sul codice fiscale RSSMRA74M55F205K: {}".format("Corretto!" if CalcCF.Calcola_Compara('RSSMRA74M55F205K') else "ERRATO!!!"))
   print ("Eseguo una verifica sul codice fiscale RSSMRA74M55F205I: {}".format("Corretto!" if CalcCF.Calcola_Compara('RSSMRA74M55F205I') else "ERRATO!!!"))
