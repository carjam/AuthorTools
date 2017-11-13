#!/usr/local/bin/python3
import re
import nltk #http://www.nltk.org/
nltk.download('cmudict')
nltk.download('punkt')
from curses.ascii import isdigit
from nltk.corpus import cmudict
import nltk.data


def normalizeText(data):
  cleaner = re.compile('[^a-z]+')
  return cleaner.sub(' ',data)


def tokenizeText(data):
  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  tokens = nltk.wordpunct_tokenize(data)
  return nltk.Text(tokens)


def wordToSyllablesDict(data):
  text = tokenizeText(data)
  words = [w.lower() for w in text]
  regexp = "[A-Za-z]+"
  exp = re.compile(regexp)
  cmud = cmudict.dict()

  syllable_dictionary={}
  for word in words:
    if exp.match(word):
      if not (word in syllable_dictionary):
        word_syllables = countSyllablesInWord(word, cmud)
        syllable_dictionary[word] = word_syllables

  return syllable_dictionary


def countSyllablesInWord(word, cmud):
  lowercase = word.lower()
  if lowercase not in cmud:
    return 0
  else:
    return max([len([y for y in x if isdigit(y[-1])]) for x in cmud[lowercase]])


def countSyllablesInText(data):
  text = tokenizeText(data)
  words = [w.lower() for w in text]

  syllable_dictionary = wordToSyllablesDict(data)

  syllable_count = 0
  for word in words:
      if word in syllable_dictionary:
        syllable_count += syllable_dictionary[word]

  return syllable_count


def countNSyllableWords(data,numSyllables):
  text = tokenizeText(data)
  words = [w.lower() for w in text]

  syllable_dictionary = wordToSyllablesDict(data)

  word_count=0
  for word in words:
      if word in syllable_dictionary:
        if syllable_dictionary[word] > numSyllables:
          word_count += 1

  return word_count


def countLetterFrequencies(data):
  letter_frequency = {}
  for letter in data:
      if letter in letter_frequency:
          letter_frequency[letter] += 1
      else:
          letter_frequency[letter] = 1
  return letter_frequency


def countWordFrequencies(data):
  word_frequency = {}
  words = nltk.word_tokenize(data)
  for word in words:
      if word in word_frequency:
          word_frequency[word] += 1
      else:
          word_frequency[word] = 1
  return word_frequency


def countWords(data):
  word_count = 0
  words = nltk.word_tokenize(data)
  return len(words)


def countSentences(data):
  sentence_count = 0
  sentences = nltk.sent_tokenize(data)
  return len(sentences) - 1

