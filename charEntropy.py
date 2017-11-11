#!/usr/bin/python
import re
import sys
from math import log

def countLetterFrequencies(data):
  letter_frequency = {}
  for letter in data:
      if letter in letter_frequency:
          letter_frequency[letter] += 1
      else:
          letter_frequency[letter] = 1
  return letter_frequency

# Function to compute the base-2 logarithm of a floating point number.
def log2(number):
    return log(number) / log(2)

# Function to normalise the text.
cleaner = re.compile('[^a-z]+')
def clean(text):
    return cleaner.sub(' ',text)

# Read and normalise input text
text = clean(sys.stdin.read().lower().strip())
letter_frequency = countLetterFrequencies(text)

# Calculate entropy
length_sum = 0.0
for letter in letter_frequency:
    probability = float(letter_frequency[letter]) / len(text)
    length_sum += probability * log2(probability)

# Output
sys.stdout.write('Entropy: %f bits per character\n' % (-length_sum))

