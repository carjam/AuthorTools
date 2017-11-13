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

  #document description
  describe = TextDescribe(content)
  char_entropy = describe.calcCharEntropy()
  sys.stdout.write('Entropy: %f bits per character\n' % (-char_entropy))

  meaningful_words = describe.meaningfulWords(1.25)
  sys.stdout.write('Meaningful words %s\n' % meaningful_words)
  
  lowinfo_words = describe.lowInfoWords(1.25)
  sys.stdout.write('\n\nLow info words %s\n' % lowinfo_words)

#profile()
main()
