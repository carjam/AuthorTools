#!/usr/local/bin/python3
import sys
from textutility import TextUtility
from wordprobability import WordProbability
from readability import Readability
from lexicaldiversity import LexicalDiversity

def profile():
  import cProfile
  cProfile.run('main()', sort='time')


def main():
  # Read and normalise input text
  content = sys.stdin.read()
  
  cleanText = TextUtility.normalizeText(content.lower().strip())
  #characters = len(cleanText)
  #sentences = TextUtility.countSentences(content)
  #words = TextUtility.countWords(content)
  #complex_words = TextUtility.countNSyllableWords(content,3)
  #syllables = TextUtility.countSyllablesInText(content)
  #sys.stdout.write('Sentences: %i\n' % (sentences))
  #sys.stdout.write('Words: %i\n' % (words))
  #sys.stdout.write('Syllables: %i\n' % (syllables))
  #sys.stdout.write('Letters: %i\n' % (characters))

  #Readability measures
  print("\n*** Readability ***")
  readability = Readability(content)
  Kincaid = readability.kincaid()
  sys.stdout.write('Kincaid (school grade level): %f\n' % (Kincaid))
  
  ARI_score = readability.ari()
  sys.stdout.write('ARI (school grade level): %f\n' % (ARI_score))
  
  ColemanLiau = readability.colemanLiau()
  sys.stdout.write('ColemanLiau (school grade level): %f\n' % (ColemanLiau))
  
  Flesch = readability.flesch()
  sys.stdout.write('Flesch: 0=12th grade, 100=4th grade %f\n' % (Flesch))
  
  Fog = readability.fog()
  sys.stdout.write('Fog: grade level: %f\n' % (Fog))
  
  SMOG = readability.smog()
  sys.stdout.write('SMOG: years of education needed to comprehend: %f\n' % (SMOG))

  print("\n*** Description ***")
  word_probability = WordProbability(content)
  hashtags = word_probability.hashtagSuggestions(99)
  sys.stdout.write('Hashtag suggestions %s\n' % hashtags)
  
  summary = word_probability.summary(99)
  sys.stdout.write('Summary %s\n' % summary)

  print("\n*** Lexical Diversity ***")
  diversity = LexicalDiversity(content)
  yulei = diversity.yulei()
  sys.stdout.write('Yule I Lexical Diversity: %f\n' % yulei)

  word_entropy = diversity.calcWordEntropy()
  sys.stdout.write('Word entropy: %f \n' % (word_entropy))

  synonym_suggestions = diversity.recommendSynonyms(99.9999,3)
  sys.stdout.write('\nHere are some synonyms for frequently occuring words:\n')
  for word in synonym_suggestions.keys():
    print(word,synonym_suggestions[word])

#profile()
main()
