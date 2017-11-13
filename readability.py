#!/usr/local/bin/python3
from TextUtility import TextUtility


def kincaid(text):
  content = text.lower().strip()
  sentences = TextUtility.countSentences(content)
  words = TextUtility.countWords(content)
  syllables = TextUtility.countSyllablesInText(content)
  
  # Kincaid = 0.39*(total_words/total_sentences) + 11.8*(total_syllables/total_words) - 15.59
  return 0.39*(words/sentences) + 11.8*(syllables/words) - 15.59


def ari(text):
  content = text.lower().strip()
  cleanText = TextUtility.normalizeText(content)
  characters = len(cleanText)
  sentences = TextUtility.countSentences(content)
  words = TextUtility.countWords(content)
  
  # ARI = 4.71*(characters/words) + 0.5*(words/sentences) - 21.43
  #https://en.wikipedia.org/wiki/Automated_readability_index
  return 4.71*(characters/words) + 0.5*(words/sentences) - 21.43


def colemanLiau(text):
  content = text.lower().strip()
  cleanText = TextUtility.normalizeText(content)
  characters = len(cleanText)
  sentences = TextUtility.countSentences(content)
  words = TextUtility.countWords(content)

  # Coleman-Liau = 5.89*(characters/words) - 30*(sentences/words) - 15.8
  #https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index
  return 5.89*(characters/words) - 30*(sentences/words) - 15.8


def flesch(text):
  content = text.lower().strip()
  sentences = TextUtility.countSentences(content)
  words = TextUtility.countWords(content)
  syllables = TextUtility.countSyllablesInText(content)

  # Flesch = 206.835 - 1.015*(total_words/total_sentences) - 84.6*(total_syllables/total_words)
  #https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
  #0 to 100, with 0 equivalent to the 12th grade and 100 equivalent to the 4th grade
  return 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)


def fog(text):
  content = text.lower().strip()
  sentences = TextUtility.countSentences(content)
  words = TextUtility.countWords(content)
  complex_words = TextUtility.countNSyllableWords(content,3)

  # Fog = 0.4*[(words/sentences) + 100*(complex_words/words)]
  #http://wiki.christophchamp.com/index.php?title=Style_and_Diction#Fog_Index_.2F_Gunning_fog_index
  return 0.4*((words/sentences) + 100*(complex_words/words))


def smog(text):
  content = text.lower().strip()
  sentences = TextUtility.countSentences(content)
  complex_words = TextUtility.countNSyllableWords(content,3)

  # SMOG = sqrt[total_complex_words * (30/total_sentences)] + 3
  #https://en.wikipedia.org/wiki/SMOG
  return (complex_words * (30/sentences))**(1/2) + 3

