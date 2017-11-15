#!/usr/local/bin/python3
import re
import nltk #http://www.nltk.org/
nltk.download('cmudict')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import cmudict
import nltk.data
from nltk.corpus import wordnet
from curses.ascii import isdigit
from memoized import memoized
from itertools import chain

class TextUtility:

  @classmethod
  @memoized
  def __getCMUDict(cls,*args):
    return cmudict.dict()


  @classmethod
  def normalizeText(cls,data):
    cleaner = re.compile('[^a-z]+')
    return cleaner.sub(' ',data)
 

  @classmethod
  def tokenizeText(cls,data):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tokens = nltk.wordpunct_tokenize(data)
    return nltk.Text(tokens)


  @classmethod
  def sentenceTokenizeText(cls,data):
    return nltk.sent_tokenize(data)


  @classmethod 
  def wordToSyllablesDict(cls,data):
    text = cls.tokenizeText(data)
    words = [w.lower() for w in text]
    regexp = "[A-Za-z]+"
    exp = re.compile(regexp)
 
    syllable_dictionary={}
    return {(word):(cls.countSyllablesInWord(word)) for word in set(words) if exp.match(word) }
 

  @classmethod
  def countSyllablesInWord(cls,word):
    lowercase = word.lower()

    cmud = cls.__getCMUDict()
    if lowercase not in cmud:
      return 0
    else:
      return max([len([y for y in x if isdigit(y[-1])]) for x in cmud[lowercase]])


  @classmethod 
  def countSyllablesInText(cls,data):
    text = cls.tokenizeText(data)
    words = [w.lower() for w in text]

    syllable_dictionary = cls.wordToSyllablesDict(data)

    syllable_count = 0
    for word in words:
        if word in syllable_dictionary:
          syllable_count += syllable_dictionary[word]

    return syllable_count


  @classmethod 
  def getNSyllableWords(cls,data,numSyllables):
    syllable_dictionary = cls.wordToSyllablesDict(data)
    return {(word):(syllable_dictionary[word]) for word in syllable_dictionary.keys() if syllable_dictionary[word] > numSyllables }


  @classmethod 
  def countNSyllableWords(cls,data,numSyllables):
    return len(cls.getNSyllableWords(data,numSyllables).keys())


  @classmethod  
  def countLetterFrequencies(cls,data):
    letter_frequency = {}
    for letter in data:
        if letter in letter_frequency:
            letter_frequency[letter] += 1
        else:
            letter_frequency[letter] = 1
    return letter_frequency


  @classmethod
  def countWordFrequencies(cls,data):
    word_frequency = {}
    words = nltk.word_tokenize(data)
    for word in words:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    return word_frequency
 
 
  @classmethod
  def countWords(cls,data):
    word_count = 0
    words = nltk.word_tokenize(data)
    return len(words) - 1


  @classmethod
  def countSentences(cls,data):
    sentence_count = 0
    sentences = nltk.sent_tokenize(data)
    return len(sentences) - 1


  @classmethod
  @memoized
  def getSynonyms(cls,word):
    sysnet_syns = wordnet.synsets(word)
    return list(set(chain.from_iterable([iter_word.lemma_names() for iter_word in sysnet_syns])).difference((word, word + 's', word + 'ing', word + 'es')))

