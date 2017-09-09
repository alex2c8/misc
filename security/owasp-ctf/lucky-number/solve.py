C = 0x29E4129E4129E413

def f(asciiSum):
	L = asciiSum - 55 * (((C * asciiSum >> 64) + ((asciiSum - (C* asciiSum >> 64)) >> 1)) >> 5)

	return L


if __name__ == '__main__':
	for i in range(0, 200):
		print i, " -> ", f(i)
