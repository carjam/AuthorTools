#!/usr/local/bin/python3
import sys
import textUtilities
import textDescribe
import readability

def profile():
  import cProfile
  cProfile.run('main()', sort='time')


def main():
  # Read and normalise input text
  content = sys.stdin.read()
  
  cleanText = textUtilities.normalizeText(content.lower().strip())
  characters = len(cleanText)
  sentences = textUtilities.countSentences(content)
  words = textUtilities.countWords(content)
  complex_words = textUtilities.countNSyllableWords(content,3)
  syllables = textUtilities.countSyllablesInText(content)
  sys.stdout.write('Sentences: %i\n' % (sentences))
  sys.stdout.write('Words: %i\n' % (words))
  sys.stdout.write('Syllables: %i\n' % (syllables))
  sys.stdout.write('Letters: %i\n' % (characters))

  #readability measures
  Kincaid = readability.kincaid(content)
  sys.stdout.write('Kincaid (school grade level): %f\n' % (Kincaid))
  
  ARI_score = readability.ari(content)
  sys.stdout.write('ARI (school grade level): %f\n' % (ARI_score))
  
  ColemanLiau = readability.colemanLiau(content)
  sys.stdout.write('ColemanLiau (school grade level): %f\n' % (ColemanLiau))
  
  Flesch = readability.flesch(content)
  sys.stdout.write('Flesch: 0=12th grade, 100=4th grade %f\n' % (Flesch))
  
  Fog = readability.fog(content)
  sys.stdout.write('Fog: grade level: %f\n' % (Fog))
  
  SMOG = readability.smog(content)
  sys.stdout.write('SMOG: years of education needed to comprehend: %f\n' % (SMOG))

  #document description
  char_entropy = textDescribe.calcCharEntropy(content)
  sys.stdout.write('Entropy: %f bits per character\n' % (-char_entropy))

  meaningful_words = textDescribe.meaningfulWords(content,1.25)
  sys.stdout.write('Meaningful words %s\n' % meaningful_words)

#profile()
main()
