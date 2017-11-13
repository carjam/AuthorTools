#!/usr/local/bin/python3
from textutility import TextUtility
import re
from math import log
import numpy

class TextDescribe(object):
  def __init__(self,text):
    self.__text = text.lower().strip()


  # Function to compute the base-2 logarithm of a floating point number.
  def __log2(self,number):
    return log(number) / log(2)


  def __is_number(self,s):
    try:
        float(s)
        return True
    except ValueError:
        return False


  def calcCharEntropy(self):
    letter_frequency = TextUtility.countLetterFrequencies(self.__text)
    length_sum = 0.0
    for letter in letter_frequency:
      probability = float(letter_frequency[letter]) / len(self.__text)
      length_sum += probability * self.__log2(probability)
    return length_sum


  def calcWordEntropy(self):
    word_frequency = TextUtility.countWordFrequencies(self.__text)
    length_sum = 0.0
    for word in word_frequency:
      probability = float(word_frequency[word]) / len(word_frequency)
      length_sum += probability * self.__log2(probability)
    return length_sum


  def __calculateEntropyContributionPerWord(self, word_frequency):

    #calculate entropy contribution per word
    word_entropies = {}
    prior_cumulative_entropy = 0
    cumulative_entropy = 0
    for word in word_frequency:
      probability = float(word_frequency[word]) / len(word_frequency)
      cumulative_entropy -= (probability * self.__log2(probability))
      entropy_contribution = cumulative_entropy - prior_cumulative_entropy

      word_entropies[word] = float(entropy_contribution) #final occurance of the word will offer best information
      prior_cumulative_entropy = cumulative_entropy

    return word_entropies


  #extract words with high information
  def meaningfulWords(self,significance):
    total_entropy = -self.calcWordEntropy()
    word_frequency = TextUtility.countWordFrequencies(self.__text) #language depedent

    #clean up noise -- language dependent
    regexp = "[A-Za-z]+"
    exp = re.compile(regexp)
    for k, v in list(word_frequency.items()):
      if not(exp.match(k)) or len(k) < 5:
        del word_frequency[k]

    word_entropies = self.__calculateEntropyContributionPerWord(word_frequency)

    #get stats on entropies
    entropies = list(word_entropies.values())
    mean = numpy.mean(entropies, axis=0)
    std_dev = numpy.std(entropies, axis=0)

    meaningful_words = []
    word_entropies = dict(sorted(word_entropies.items(), key=lambda k: k[1], reverse=True))
    for word in word_entropies:
      entropy = word_entropies[word]
      if self.__is_number(entropy) and not (entropy==0) :
        if (float(mean) + float(std_dev*significance)) <= float(entropy):
          if not (word in meaningful_words):
            meaningful_words.append(word) 

    return set(meaningful_words)

  #extract words with low information
  def lowInfoWords(self,significance):
    total_entropy = -self.calcWordEntropy()
    word_frequency = TextUtility.countWordFrequencies(self.__text) #language depedent

    #clean up noise -- language dependent
    regexp = "[A-Za-z]+"
    exp = re.compile(regexp)
    for k, v in list(word_frequency.items()):
      if not(exp.match(k)):
        del word_frequency[k]
    
    word_entropies = self.__calculateEntropyContributionPerWord(word_frequency)

    #get stats on entropies
    entropies = list(word_entropies.values())
    mean = numpy.mean(entropies, axis=0)
    std_dev = numpy.std(entropies, axis=0)

    lowinfo_words = []
    word_entropies = dict(sorted(word_entropies.items(), key=lambda k: k[1], reverse=True))
    for word in word_entropies:
      entropy = word_entropies[word]
      if self.__is_number(entropy) and not (entropy==0) :
        if (float(mean) + float(std_dev*significance)) > float(entropy):
          if not (word in lowinfo_words):
            lowinfo_words.append(word) 

    return set(lowinfo_words)

