import numpy as np
import matplotlib.pyplot as plt
import re

s = str(open("babylon.txt", "rt").readline())

_s = re.sub('[0-9]', '', s)

print(_s)

import sys
sys.exit(0)

sd = sorted(s)
u, c = np.unique(sd, return_counts=True)
d = dict(zip(u, c))
#d = sorted(d, key=lambda k : k[1])

"""
print(d['b'])
print(d['a'])
print(d['b'])
print(d['y'])
print(d['l'])
print(d['o'])
print(d['n'])
"""

for x, y in d.items():
    print(x, y)

plt.bar(d.keys(), d.values())
plt.show()
