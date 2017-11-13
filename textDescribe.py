#!/usr/local/bin/python3
import textUtilities
import re
from math import log
import numpy


# Function to compute the base-2 logarithm of a floating point number.
def log2(number):
  return log(number) / log(2)


def is_number(s):
  try:
      float(s)
      return True
  except ValueError:
      return False


def calcCharEntropy(text):
  data = text.lower().strip()
  letter_frequency = textUtilities.countLetterFrequencies(data)
  length_sum = 0.0
  for letter in letter_frequency:
    probability = float(letter_frequency[letter]) / len(data)
    length_sum += probability * log2(probability)
  return length_sum


def calcWordEntropy(text):
  data = text.lower().strip()
  word_frequency = textUtilities.countWordFrequencies(data)
  length_sum = 0.0
  for word in word_frequency:
    probability = float(word_frequency[word]) / len(word_frequency)
    length_sum += probability * log2(probability)
  return length_sum


#blind contextual classification of text
#should be generalizable to any language given a means of tokenization
def meaningfulWords(text, significance):
  data = text.lower().strip()
  total_entropy = -calcWordEntropy(data)
  word_frequency = textUtilities.countWordFrequencies(data) #language depedent

  #clean up noise -- language dependent
  regexp = "[A-Za-z]+"
  exp = re.compile(regexp)
  for k, v in list(word_frequency.items()):
    if not(exp.match(k)) or len(k) < 5:
      del word_frequency[k]

  word_entropies = {}
  prior_cumulative_entropy = 0
  cumulative_entropy = 0
  for word in word_frequency:
    probability = float(word_frequency[word]) / len(word_frequency)
    cumulative_entropy -= (probability * log2(probability))
    entropy_contribution = cumulative_entropy - prior_cumulative_entropy

    word_entropies[word] = float(entropy_contribution) #final occurance of the word will offer best information
    prior_cumulative_entropy = cumulative_entropy

  entropies = list(word_entropies.values())
  mean = numpy.mean(entropies, axis=0)
  std_dev = numpy.std(entropies, axis=0)

  meaningful_words = []
  word_entropies = dict(sorted(word_entropies.items(), key=lambda k: k[1], reverse=True))
  for word in word_entropies:
    entropy = word_entropies[word]
    if is_number(entropy) and not (entropy==0) :
      if (float(mean) + float(std_dev*significance)) <= float(entropy):
        if not (word in meaningful_words):
          meaningful_words.append(word) 

  return meaningful_words

