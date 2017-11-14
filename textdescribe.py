#!/usr/local/bin/python3
from textutility import TextUtility
import re
from math import log
from math import e
import numpy
from memoized import memoized

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
      probability = float(letter_frequency[letter]) / sum(letter_frequency.values())
      length_sum -= probability * self.__log2(probability)
    return length_sum


  def calcWordEntropy(self):
    word_frequency = TextUtility.countWordFrequencies(self.__text)
    length_sum = 0.0
    for word in word_frequency.keys():
      probability = float(word_frequency[word]) / sum(word_frequency.values())
      length_sum -= probability * self.__log2(probability)
    return length_sum


  @memoized
  def __calculateWordProbabilities(self):
    word_frequency = TextUtility.countWordFrequencies(self.__text) #language depedent

    #clean up noise -- language dependent
    MIN_CHARS = 5
    regexp = "[A-Za-z]+"
    exp = re.compile(regexp)
    for k, v in list(word_frequency.items()):
      if not(exp.match(k)) or len(k) < MIN_CHARS:
        del word_frequency[k]

    word_probabilities = {}
    for word in word_frequency.keys():
      entropy_contribution = float(word_frequency[word]) / sum(word_frequency.values()) 
      word_probabilities[word] = float(entropy_contribution) #final occurance of the word will offer best information

    return word_probabilities.items()


  #extract words with high information
  def probableWords(self,significance):
    word_probabilities = dict(self.__calculateWordProbabilities())

    #get stats on entropies
    probabilities = list(word_probabilities.values())
    mean = numpy.mean(probabilities, axis=0)
    std_dev = numpy.std(probabilities, axis=0)

    highinfo_words = []
    word_probabilities = dict(sorted(word_probabilities.items(), key=lambda k: k[1], reverse=True))
    for word in word_probabilities:
      probability = word_probabilities[word]
      if self.__is_number(probability) and not (probability > 0) :
        if (float(mean) + float(std_dev*significance)) >= float(probability):
          highinfo_words.append(word) 

    return set(highinfo_words)


  #extract words with low information
  def unlikelyWords(self,significance):
    word_probabilities = dict(self.__calculateWordProbabilities())

    #get stats on probabilities
    probabilities = list(word_probabilities.values())
    mean = numpy.mean(probabilities, axis=0)
    std_dev = numpy.std(probabilities, axis=0)

    lowinfo_words = []
    word_probabilities = dict(sorted(word_probabilities.items(), key=lambda k: k[1], reverse=True))
    for word in word_probabilities:
      probability = word_probabilities[word]
      if self.__is_number(probability) and not (probability==0) :
        if (float(mean) + float(std_dev*significance)) < float(probability):
          lowinfo_words.append(word) 

    return set(lowinfo_words)

 
  def hashtagSuggestions(self,significance):
    hashtags = list(self.unlikelyWords(significance))
    hashtags[:] = ['#' + word for word in hashtags]
    return hashtags


  def summary(self,significance):
    sentences = TextUtility.sentenceTokenizeText(self.__text)
    words = self.unlikelyWords(significance)
    result=[]
    for sentence in sentences:
      word_match = 0
      for word in words:
        if word in sentence:
          word_match += 1
          if word_match > 2 and len(sentence) < 150 and sentence not in result:
            result.append(sentence)
    
    if len(result) == 0:
      result.append('None available')
    return result
