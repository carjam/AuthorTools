#!/usr/local/bin/python3

class Plagarism:
  # https://www.geeksforgeeks.org/searching-for-patterns-set-3-rabin-karp-algorithm/
  # Following program is the python implementation of
  # Rabin Karp Algorithm given in CLRS book

 
  # pat  -> pattern
  # txt  -> text
  def rabinKarp(self, pat, txt):
    # d is the number of characters in the input alphabet
    q = 101 # a prime number
    d = 256
    patternLen = len(pat)
    txtLen = len(txt)
    i = 0
    j = 0
    patternHash = 0    # hash value for pattern
    txtHash = 0    # hash value for txt
    h = 1

    # The value of h would be "pow(d, M-1)%q"
    for i in range(patternLen-1):
      h = (h*d)%q

    # Calculate the hash value of pattern and first window
    # of text
    for i in range(patternLen):
      patternHash = (d*patternHash + ord(pat[i]))%q
      txtHash = (d*txtHash + ord(txt[i]))%q

    # Slide the pattern over text one by one
    for i in range(txtLen-patternLen+1):
      # Check the hash values of current window of text and
      # pattern if the hash values match then only check
      # for characters on by one
      if patternHash==txtHash:
        # Check for characters one by one
        for j in range(patternLen):
          if txt[i+j] != pat[j]:
            break

        j+=1
        # if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
        if j==patternLen:
          #print 'Pattern found at index ' + str(i)
          return i

      # Calculate hash value for next window of text: Remove
      # leading digit, add trailing digit
      if i < txtLen-patternLen:
        txtHash = (d*(txtHash-ord(txt[i])*h) + ord(txt[i+patternLen]))%q

        # We might get negative values of t, converting it to
        # positive
        if txtHash < 0:
          txtHash = txtHash+q

