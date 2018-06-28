#!/usr/local/bin/python3
from bloomfilter import BloomFilter

class Plagarism:
  def rabinKarp(self, patterns, txt, acceptableRateFalsePos):
    if (not txt or not patterns):
        raise ValueError('Search requires text and a pattern')

    q = 101 # a prime number
    d = 256
    h = 1

    matches = dict()
    for p in patterns:
        matches[p] = []

    patternHashes = []
    patternLen = len(next(iter(patterns))) #length of first pattern
    txtLen = len(txt)

    if (txtLen < patternLen):
        raise ValueError('A pattern longer than text to search cannot exist in the text.')

    # The value of h would be "pow(d, M-1)%q"
    for i in range(patternLen-1):
      h = (h*d)%q

    numPat = len(patterns)
    if (numPat < 1):
        raise ValueError('Search requires a pattern')

    for pat in set(patterns):
        if (patternLen != len(pat)):
            raise ValueError('Search only supports a fixed length pattern match.')

        patternHash = 0
        for i in range(patternLen):
            patternHash = (d*patternHash + ord(pat[i]))%q
        patternHashes.append(patternHash)
    bloomf = BloomFilter(patternHashes)

    # setup the first comparison based on length of pattern
    left = 0
    right = patternLen
    txtHash = 0
    for j in range(patternLen):
      txtHash = (d*txtHash + ord(txt[j]))%q

    #scoot through txt 1 char at a time
    while (right <= txtLen):
        if (bloomf.contains(txtHash)):
            if (txt[left:right] in patterns):
                matches[txt[left:right]].append(left)
        if(left+patternLen < txtLen):
            txtHash = (d*(txtHash-ord(txt[left])*h) + ord(txt[left+patternLen]))%q
        left += 1
        right += 1

    return matches

