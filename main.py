#!/usr/local/bin/python3
import sys
from textutility import TextUtility
from textdescribe import TextDescribe
from readability import Readability

def profile():
  import cProfile
  cProfile.run('main()', sort='time')


def main():
  # Read and normalise input text
  content = sys.stdin.read()
  
  cleanText = TextUtility.normalizeText(content.lower().strip())
  characters = len(cleanText)
  sentences = TextUtility.countSentences(content)
  words = TextUtility.countWords(content)
  complex_words = TextUtility.countNSyllableWords(content,3)
  syllables = TextUtility.countSyllablesInText(content)
  sys.stdout.write('Sentences: %i\n' % (sentences))
  sys.stdout.write('Words: %i\n' % (words))
  sys.stdout.write('Syllables: %i\n' % (syllables))
  sys.stdout.write('Letters: %i\n' % (characters))

  #Readability measures
  Kincaid = Readability.kincaid(content)
  sys.stdout.write('Kincaid (school grade level): %f\n' % (Kincaid))
  
  ARI_score = Readability.ari(content)
  sys.stdout.write('ARI (school grade level): %f\n' % (ARI_score))
  
  ColemanLiau = Readability.colemanLiau(content)
  sys.stdout.write('ColemanLiau (school grade level): %f\n' % (ColemanLiau))
  
  Flesch = Readability.flesch(content)
  sys.stdout.write('Flesch: 0=12th grade, 100=4th grade %f\n' % (Flesch))
  
  Fog = Readability.fog(content)
  sys.stdout.write('Fog: grade level: %f\n' % (Fog))
  
  SMOG = Readability.smog(content)
  sys.stdout.write('SMOG: years of education needed to comprehend: %f\n' % (SMOG))

  #document description
  char_entropy = TextDescribe.calcCharEntropy(content)
  sys.stdout.write('Entropy: %f bits per character\n' % (-char_entropy))

  meaningful_words = TextDescribe.meaningfulWords(content,1.25)
  sys.stdout.write('Meaningful words %s\n' % meaningful_words)

#profile()
main()
