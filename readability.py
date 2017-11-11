#!/usr/local/bin/python3
import re
import nltk #http://www.nltk.org/
nltk.download('cmudict')
nltk.download('punkt')
from curses.ascii import isdigit
from nltk.corpus import cmudict
import nltk.data
import pprint
import sys

def normalizeText(data):
  cleaner = re.compile('[^a-z]+')
  return cleaner.sub(' ',data)


def tokenizeText(data):
  tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
  tokens = nltk.wordpunct_tokenize(data)
  return nltk.Text(tokens)


def wordToSyllablesDict(data):
  #text = tokenizeText(data)
  text = data.split()
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


def countSyllablesInText(data,syllable_dictionary):
  #text = tokenizeText(data)
  text = data.split()
  words = [w.lower() for w in text]

  syllable_count = 0
  for word in words:
      if word in syllable_dictionary:
        syllable_count += syllable_dictionary[word]

  return syllable_count


def countNSyllableWords(data,syllables,syllable_dictionary):
  #text = tokenizeText(data)
  text = data.split()
  words = [w.lower() for w in text]

  word_count=0
  for word in words:
      if word in syllable_dictionary:
        if syllable_dictionary[word] > syllables:
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


def countWords(data):
  word_count = 0
  #words = nltk.word_tokenize(data)
  words = data.split()
  return len(words)


def countSentences(data):
  sentence_count = 0
  #sentences = nltk.sent_tokenize(data)
  sentences = data.split('.')
  return len(sentences) - 1


def kincaid(words, sentences, syllables):
  # Kincaid = 0.39*(total_words/total_sentences) + 11.8*(total_syllables/total_words) - 15.59
  return 0.39*(words/sentences) + 11.8*(syllables/words) - 15.59


def ari(characters, words, sentences):
  # ARI = 4.71*(characters/words) + 0.5*(words/sentences) - 21.43
  return 4.71*(characters/words) + 0.5*(words/sentences) - 21.43


def colemanLiau(characters, words, sentences):
  # Coleman-Liau = 5.89*(characters/words) - 30*(sentences/words) - 15.8
  #https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index
  return 5.89*(characters/words) - 30*(sentences/words) - 15.8

def flesch(words, sentences, syllables):
  # Flesch = 206.835 - 1.015*(total_words/total_sentences) - 84.6*(total_syllables/total_words)
  #https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
  #0 to 100, with 0 equivalent to the 12th grade and 100 equivalent to the 4th grade
  return 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)

def fog(words, sentences, complex_words):
  # Fog = 0.4*[(words/sentences) + 100*(complex_words/words)]
  #http://wiki.christophchamp.com/index.php?title=Style_and_Diction#Fog_Index_.2F_Gunning_fog_index
  return 0.4*((words/sentences) + 100*(complex_words/words))


def smog(complex_words, sentences):
  # SMOG = sqrt[total_complex_words * (30/total_sentences)] + 3
  #https://en.wikipedia.org/wiki/SMOG
  return (complex_words * (30/sentences))**(1/2) + 3


def profile():
  import cProfile
  cProfile.run('main()', sort='time')


def main():
  # Read and normalise input text
  content = sys.stdin.read().lower().strip()
  cleanText = normalizeText(content)
  
  characters = len(cleanText)
  #letter_frequency = countLetterFrequencies(cleanText) 
  sentences = countSentences(content)
  words = countWords(content)
  
  syllable_words = wordToSyllablesDict(content)
  complex_words = countNSyllableWords(content,3,syllable_words)
  syllables = countSyllablesInText(content,syllable_words)
  
  sys.stdout.write('Sentences: %i\n' % (sentences))
  sys.stdout.write('Words: %i\n' % (words))
  sys.stdout.write('Syllables: %i\n' % (syllables))
  sys.stdout.write('Letters: %i\n' % (characters))

  Kincaid = kincaid(words,sentences,syllables)
  sys.stdout.write('Kincaid (school grade level): %f\n' % (Kincaid))
  
  ARI_score = ari(characters,words,sentences)
  sys.stdout.write('ARI (school grade level): %f\n' % (ARI_score))
  
  ColemanLiau = colemanLiau(characters, words, sentences)
  sys.stdout.write('ColemanLiau (school grade level): %f\n' % (ColemanLiau))
  
  Flesch = flesch(words,sentences,syllables)
  sys.stdout.write('Flesch: 0=12th grade, 100=4th grade %f\n' % (Flesch))
  
  Fog = fog(words, sentences, complex_words)
  sys.stdout.write('Fog: grade level: %f\n' % (Fog))
  
  SMOG = smog(complex_words, sentences)
  sys.stdout.write('SMOG: years of education needed to comprehend: %f\n' % (SMOG))


#profile()
main()
