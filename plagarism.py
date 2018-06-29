#!/usr/local/bin/python3
from bloomfilter import BloomFilter

class Plagarism:
  def rabinKarp(self, patterns, txt):
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


  #wildcard pattern search based on rabin-karp
  def wildCardSearch(self, pattern, txt):
    wildcard = '*'
    patterns = pattern.split(wildcard)

    if len(patterns) < 2:
        raise ValueError('Wildcard search requires a wildcard')

    # rabinKarp only allows for fixed len search so pull minimum length eminating from wildcard outward
    i = 0
    prunedPatterns =[] 
    contiguous = dict()
    minLen = min([len(pat) for pat in patterns])
    for pat in patterns:
        if not pat:
            continue
        prunedPat = pat[-minLen:] if i%2==0 else pat[:minLen]
        prunedPatterns.append(prunedPat)
        contiguous[prunedPat] = [] #setup key:[empty] for our matches
        i+=1
    wild = self.rabinKarp(set(prunedPatterns), txt)
    if not wild[prunedPatterns[i-1]] or not wild[prunedPatterns[0]]:
        return

    #loop over patterns in order to find contiguous matches
    lastLastHit = max(v for v in wild[prunedPatterns[i-1]])
    lastFirstHit = max(v for v in wild[prunedPatterns[0]] if v < lastLastHit)
    firstHit=0
    while True:
        j=0
        for pat in patterns:
            if not pat:
                continue
            prunedPat = prunedPatterns[j]
            firstHit = min(v for v in wild[prunedPat] if v > firstHit) #change this to a queue with pop to avoid per iteration search

            #check back vs actual test for a full match
            patLen=len(pat)
            lenDiff=patLen-minLen
            for k in range(patLen):
            #we know that prunedPat matches text so don't search the whole thing:
            #'this is a test' with prunedPat = 'est' => from: firstHit - (patLen-minLen) to: firstHit
            #'this is a test' with prunedPat = 'tes' => from: firstHit + minLen to: firstHit + patLen
                if pat[k] != txt[firstHit+k-lenDiff]:
                    break

            if k == patLen-1:
                contiguous[prunedPat].append(firstHit)

            j+=1
        if j >= i-1 and firstHit >= lastFirstHit:
            break

    return contiguous
