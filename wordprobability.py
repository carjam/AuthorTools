#!/usr/local/bin/python3
from textutility import TextUtility
import re
import numpy
from memoized import memoized
from sklearn.feature_extraction.text import TfidfVectorizer


class WordProbability(object):
  def __init__(self,text):
    self.__tu = TextUtility(text)


  def __is_number(self,s):
    try:
        float(s)
        return True
    except ValueError:
        return False


  '''Word Probability'''
  @memoized
  def __calculateWordProbabilities(self):
    word_frequency = self.__tu.countWordFrequencies()
    word_count = self.__tu.countWords()

    word_probabilities = {}
    for word in word_frequency.keys():
        word_probabilities[word] = float(word_frequency[word] / word_count) 

    return word_probabilities.items()


  #extract words with high information
  def wordsAbovePercentile(self,percentile):
    word_probabilities = dict(self.__calculateWordProbabilities())

    probabilities = list(word_probabilities.values())
    percentile_score = numpy.percentile(probabilities,percentile,axis=0, interpolation='lower')

    highinfo_words = []
    word_probabilities = dict(sorted(word_probabilities.items(), key=lambda k: k[1], reverse=True))
    for word in word_probabilities:
      probability = word_probabilities[word]
      if self.__is_number(probability) and probability > 0 :
        if percentile_score <= float(probability):
          highinfo_words.append(word) 

    return set(highinfo_words)


  #extract words with low information
  def wordsBelowPercentile(self,percentile):
    word_probabilities = dict(self.__calculateWordProbabilities())

    probabilities = list(word_probabilities.values())
    percentile_score = numpy.percentile(probabilities,percentile,axis=0, interpolation='lower')

    lowinfo_words = []
    word_probabilities = dict(sorted(word_probabilities.items(), key=lambda k: k[1], reverse=True))
    for word in word_probabilities:
      probability = word_probabilities[word]
      if self.__is_number(probability) and probability > 0 :
        if percentile_score > float(probability):
          lowinfo_words.append(word) 

    return set(lowinfo_words)

 
  def hashtagSuggestions(self,percentile):
    wordsA = list(self.wordsAbovePercentile(percentile))
    wordsB = list(self.wordsBelowPercentile(100-percentile))
    hashtags = wordsA + wordsB

    hashtags[:] = ['#' + word for word in hashtags]
    return hashtags


  def summary(self,percentile):
    sentences = self.__tu.sentenceTokenizeText()
    words = self.tfidf(5)

    result=[]
    for sentence in sentences:
      word_match = 0
      for word in words:
        if word in sentence:
          word_match += 1
          if word_match > 1 and len(sentence) < 150 and sentence not in result:
            result.append(sentence)

    if len(result) == 0:
      result.append('None available')
    return result

  def tfidf(self, numToReturn):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([' '.join(self.__tu.tokenizeAndRemoveCommonWords(3))])

    result = dict()
    feature_names = vectorizer.get_feature_names()
    for col in tfidf.nonzero()[1]:
        result[feature_names[col]] = tfidf[0, col]

    return sorted(result, key=result.get, reverse=True)[:numToReturn]

