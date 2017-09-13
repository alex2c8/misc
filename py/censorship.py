#!/usr/bin/python -u

import base64, SocketServer, os, sys, hashlib, signal
from Crypto.PublicKey import RSA

def text_to_num(s):
	return int(s.encode('hex'), 16)


PLAIN_FLAG = open("/home/censorship/flag_part2.txt", "r").read().strip()



if __name__ == "__main__":

    def fail(message):
        sys.stdout.write (message + "\nGood-bye.\n")
        return False

    def captcha():
        proof = base64.b64encode(os.urandom(9))
        sys.stdout.write(proof)
        test = raw_input()
        ha = hashlib.sha1()
        ha.update(test)
        if test[0:12] != proof or not ha.digest().endswith('\xFF'*3):
        	return fail("To pass the first part you must read the code and pass this Proof-Of-Work!")
	else:
		POW_FLAG = open("/home/censorship/flag_part1.txt", "r").read().strip()
		sys.stdout.write("You passed! %s\n" % POW_FLAG)

	return True

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

    def handle():
        if not captcha():
		return

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
    signal.alarm(120)
    handle()

