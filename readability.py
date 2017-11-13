#!/usr/local/bin/python3
from textutility import TextUtility

class Readability:
  COMPLEX_WORD_SYLLABLES = 3

  def __init__(self,text):
    self.__text = text.lower().strip()
    self.__sentences = TextUtility.countSentences(self.__text)
    self.__words = TextUtility.countWords(self.__text)
    cleanText = TextUtility.normalizeText(self.__text)
    self.__characters = len(cleanText)
    self.__syllables = TextUtility.countSyllablesInText(self.__text)
    self.__complex_words = TextUtility.countNSyllableWords(self.__text,self.COMPLEX_WORD_SYLLABLES)


  def kincaid(self):
    # Kincaid = 0.39*(total_words/total_sentences) + 11.8*(total_syllables/total_words) - 15.59
    return 0.39*(self.__words/self.__sentences) + 11.8*(self.__syllables/self.__words) - 15.59
 
 
  def ari(self):
    # ARI = 4.71*(characters/words) + 0.5*(words/sentences) - 21.43
    #https://en.wikipedia.org/wiki/Automated_readability_index
    return 4.71*(self.__characters/self.__words) + 0.5*(self.__words/self.__sentences) - 21.43
 
 
  def colemanLiau(self):
    # Coleman-Liau = 5.89*(characters/words) - 30*(sentences/words) - 15.8
    #https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index
    return 5.89*(self.__characters/self.__words) - 30*(self.__sentences/self.__words) - 15.8
 
 
  def flesch(self):
    # Flesch = 206.835 - 1.015*(total_words/total_sentences) - 84.6*(total_syllables/total_words)
    #https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
    #0 to 100, with 0 equivalent to the 12th grade and 100 equivalent to the 4th grade
    return 206.835 - 1.015*(self.__words/self.__sentences) - 84.6*(self.__syllables/self.__words)
 

  def fog(self):
    # Fog = 0.4*[(words/sentences) + 100*(complex_words/words)]
    #http://wiki.christophchamp.com/index.php?title=Style_and_Diction#Fog_Index_.2F_Gunning_fog_index
    return 0.4*((self.__words/self.__sentences) + 100*(self.__complex_words/self.__words))
 
 
  def smog(self):
    # SMOG = sqrt[total_complex_words * (30/total_sentences)] + 3
    #https://en.wikipedia.org/wiki/SMOG
    return (self.__complex_words * (30/self.__sentences))**(1/2) + 3
 
