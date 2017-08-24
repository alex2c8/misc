#!/usr/bin/python
import struct, sys
 
def dw(i):
	return struct.pack("<I", i)
 