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

  def __init__(self,text):
    self.__text = text.lower().strip()    


  @classmethod
  @memoized
  def __getCMUDict(cls,*args):
    return cmudict.dict()


  def normalizeText(self):
    cleaner = re.compile('[^a-z]+')
    return cleaner.sub(' ',self.__text)

  @memoized
  def tokenizeAndRemoveCommonWords(self, minchars):
    #remove short or non-alpha characters
    words = self.tokenizeText()
    txt = [w.lower() for w in words]

    regexp = "[A-Za-z]+"
    exp = re.compile(regexp)
    result = [v for v in txt if (exp.match(v) and len(v) >= minchars)]
    return ' '.join(result).split()

  @memoized
  def tokenizeText(self):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    tokens = nltk.wordpunct_tokenize(self.__text)
    return nltk.Text(tokens)

  @memoized
  def sentenceTokenizeText(self):
    return nltk.sent_tokenize(self.__text)


  def wordToSyllablesDict(self):
    text = self.tokenizeText()
    words = [w.lower() for w in text]
    regexp = "[A-Za-z]+"
    exp = re.compile(regexp)
 
    syllable_dictionary={}
    return {(word):(TextUtility.countSyllablesInWord(word)) for word in set(words) if exp.match(word) }
 

  @classmethod
  def countSyllablesInWord(cls,word):
    lowercase = word.lower()

    cmud = cls.__getCMUDict()
    if lowercase not in cmud:
      return 0
    else:
      return max([len([y for y in x if isdigit(y[-1])]) for x in cmud[lowercase]])


  def countSyllablesInText(self):
    text = self.tokenizeText()
    words = [w.lower() for w in text]

    syllable_dictionary = self.wordToSyllablesDict()

    syllable_count = 0
    for word in words:
        if word in syllable_dictionary:
          syllable_count += syllable_dictionary[word]

    return syllable_count


  def getNSyllableWords(self,numSyllables):
    syllable_dictionary = self.wordToSyllablesDict()
    return {(word):(syllable_dictionary[word]) for word in syllable_dictionary.keys() if syllable_dictionary[word] > numSyllables }


  def countNSyllableWords(self,numSyllables):
    return len(self.getNSyllableWords(numSyllables).keys())


  def countLetterFrequencies(self):
    letter_frequency = {}
    for letter in self.__text:
        if letter in letter_frequency:
            letter_frequency[letter] += 1
        else:
            letter_frequency[letter] = 1
    return letter_frequency


  def countWordFrequencies(self):
    word_frequency = {}
    #words = self.tokenizeText()
    words = self.tokenizeAndRemoveCommonWords(5)
    for word in words:
        if word in word_frequency:
            word_frequency[word] += 1
        else:
            word_frequency[word] = 1
    return word_frequency
 
  def countWords(self):
    word_count = 0
    #words = self.tokenizeText()
    words = self.tokenizeAndRemoveCommonWords(5)
    return len(words)


  def countSentences(self):
    sentence_count = 0
    sentences = self.sentenceTokenizeText()
    return len(sentences)


  @classmethod
  @memoized
  def getSynonyms(cls,word):
    sysnet_syns = wordnet.synsets(word)
    return list(set(chain.from_iterable([iter_word.lemma_names() for iter_word in sysnet_syns])).difference((word, word + 's', word + 'ing', word + 'es')))

