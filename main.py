#!/usr/local/bin/python3
import sys
from textutility import TextUtility
from wordprobability import WordProbability
from readability import Readability
from lexicaldiversity import LexicalDiversity
from search import TextSearch

def profile():
  import cProfile
  cProfile.run('main()', sort='time')


def main():
  # Read and normalise input text
  content = sys.stdin.read()
  tu = TextUtility(content)
  cleanText = tu.normalizeText()

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

  print("\n*** Lexical Diversity ***")
  diversity = LexicalDiversity(content)
  yulei = diversity.yulei()
  sys.stdout.write('Yule I Lexical Diversity: %f\n' % yulei)

  word_entropy = diversity.calcWordEntropy()
  sys.stdout.write('Word entropy: %f \n' % (word_entropy))

  synonym_suggestions = diversity.recommendSynonyms(95,3)
  sys.stdout.write('\nHere are some synonyms for frequently occuring words:\n')
  for word in synonym_suggestions.keys():
    print(word,synonym_suggestions[word])


  print("\n*** Description ***")
  word_probability = WordProbability(content)
  hashtags = word_probability.hashtagSuggestions(99)
  sys.stdout.write('Hashtag suggestions %s\n' % hashtags)
  
  summary = word_probability.summary(55)
  sys.stdout.write('\nSummary %s\n' % summary)

  print("\n*** Plagarism ***")
  plagarism = TextSearch()
  txt = content 
  pat = "empowers consumers to take control"
  setPat = { "empowers consumers", "a million bank acc", "Contact UsPrivacy " }

  plg = plagarism.rabinKarp(setPat,txt)
  sys.stdout.write('Rabin-Karp found pattern at %s \n' % str(plg))

  #wildSearch = 'tsfd;lkasdi*ghasd'
  wildSearch = 'the*est'
  #empowers consumers to take control of their financial
  #wildSearch = 'empowers c*to take*of their financial'
  #wildSearch = 'consumers*take control of their'
  wild = plagarism.wildCardSearch(wildSearch, txt)
  sys.stdout.write('Wildcard search found %s \n' % str(wild))

  plagarism.findCliches(content)

#profile()
main()
