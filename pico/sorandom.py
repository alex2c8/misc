#!/usr/bin/python -u
import random,string

flag = "FLAG:"+open("flag", "r").read()[:-1]
encflag = ""
random.seed("random")
for c in flag:
  if c.islower():
    #rotate number around alphabet a random amount
    x = random.randrange(0,26)
    encflag += chr((ord(c)-ord('a')+x)%26 + ord('a'))
    print "lower: " + str(x)
  elif c.isupper():
    y = random.randrange(0,26)
    encflag += chr((ord(c)-ord('A')+y)%26 + ord('A'))
    print "upper: " + str(y)
  elif c.isdigit():
    z = random.randrange(0,10)
    encflag += chr((ord(c)-ord('0')+z)%10 + ord('0'))
    print "digit: " + str(z)
  else:
    encflag += c
print "Unguessably Randomized Flag: "+encflag
