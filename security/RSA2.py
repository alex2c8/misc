#!/usr/bin/python -u

import base64, SocketServer, os, sys, hashlib, signal
from Crypto.PublicKey import RSA

def text_to_num(s):
	return int(s.encode('hex'), 16)

def trial(FLAG, N, e, d):
	sys.stdout.write("Input a number and we shall serve you!\n")

	user_input = raw_input()
	try:
		input = int(user_input)
	except:
		return False

	result = pow(input, d, N)
	if result == FLAG or result == (N - FLAG) :
		sys.stdout.write("It can't be this simple, right?!\n")
	else:
	    sys.stdout.write( str(result) + "\n" )

	return True

if __name__ == "__main__":

	PLAIN_FLAG = open("flag.txt", "r").read().strip()  
	FLAG = text_to_num(os.urandom(10) + PLAIN_FLAG + os.urandom(10) )

	rsa = RSA.generate(1024, os.urandom)
	N = getattr(rsa,'n')
	e = getattr(rsa,'e')
	d = getattr(rsa,'d')

	assert pow( pow(1234, e, N), d, N) == 1234


	banner = "Welcome to our trial RSA service! Currently we offer 2 free decryptions.\n"
	banner += "How about a free ciphertext too? %s\n" % pow(FLAG, e, N)

	sys.stdout.write(banner)
	for i in range(2):
		if not trial(FLAG, N, e, d):
			break


