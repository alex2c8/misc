import socket
import sys
import subprocess
import time

remote_ip = '127.0.0.1'
remote_port = 2222

buf_size = 1024

def send(i):
    # proc = subprocess.Popen(["./greek_to_me.exe"])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remote_ip, remote_port))
    s.send(chr(i))
    data = s.recv(buf_size)
    s.close()

    print "sent", i
    print "recvd", data

    proc.kill()

def main():
    for i in range(1, 256, 1):
        send(i)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remote_ip, remote_port))
    s.send(chr(162))
    # i = 162
