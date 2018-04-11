"""
After loading the pcap file, one can see that there is a pattern in the recorded scenario.
The client accessed 44 pages from the server (len(FLAG) == 44) and because the server consists of ascii chars,
it is now clear that the client accessed the pages corresponding to the chars in the flag.
And there's also another hint: on each page there is a number of '#'. So the page name is tied to its length (e.g. 'a' has 10 bytes).
Therefore, we can look at the accesses that the client has made and wrote down the length of the returned page.
This length also accounts for extra information (24 bytes in our case).
We know that the flag has the format CRYPTO_CTF{md5sum}, so we can look for 32 accesses that correspond to the hex values of the md5sum (because we know the rest).
The array 'lengths' in this script contains the lengths of those pages. Remove 24 and convert to hex-chars and we got the md5sum.

In wireshark, select as filter: ssl.app_data && ip.src == 141.85.224.115.
Look under Secure Sockets Layer, last TLSv1.2 Record Layer: Application Data Protocol: http-over-tls.
We can see that going through requests, the length field changes.
If the length of the page is 0, this entry is non-existent.
"""

import urllib.request
import requests
import pickle

FLAG = "CRYPTO_CTF{098f6bcd4621d373cade4e832627b4f6}"

URL = "https://141.85.224.115"

char_from = ord("!")
char_to = ord("~")

generate = False

if generate:
    data = {}

    for c in range(char_from, char_to + 1):
        link = URL + "/data?page=%" + hex(c)[2:]
        x = requests.get(link, verify=False)
        data[chr(c)] = x.text
        print(char_to - c)

    pickle.dump(data, open("data.pkl", "wb"))
else:
    data = pickle.load(open("data.pkl", "rb"))

    for k, v in data.items():
        count = v.count("#")
        print(k, "\t", hex(count)[2:], "\t",  count)


extra = 24
lengths = [32, 37, 39, 0, 27, 27, 39, 28, 34, 38, 33, 26, 36, 26, 25, 27, 0, 28, 26, 30, 35, 0, 28, 38, 26, 35, 27, 29, 35, 26, 26, 27]
hex_vals = list(map(lambda x : 0 if x == 0 else x - extra, lengths))
hex_vals = list(map(lambda x : hex(x)[2:], hex_vals))
hex_vals = "".join(hex_vals)

flag = "CRYPTO_CTF{" + hex_vals + "}"

print(flag)
