import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import shuffle
import sys
from operator import itemgetter

width = 1280
height = 720

bs = 40

bh = 720 // bs
bw = 1280 // bs

# BGR
img = cv2.imread("jigsaw.png", 0)

blocks = []

means = {}

for i in range(bh):
    for j in range(bw):
        block = img[i*bs : (i+1)*bs, j*bs : (j+1)*bs]
        blocks.append(block)

        means[(i, j)] = round(img[i*bs: (i+1)*bs, j*bs: (j+1)*bs].mean(), 3)


sorted_means = dict(sorted(means.items(), key=itemgetter(1)))

nimg = np.zeros_like(img)
ii = jj = 0
for idx, _ in sorted_means.items():
    (i, j) = idx
    print(i, j)

    nimg[ii*bs: (ii+1)*bs, jj*bs: (jj+1)*bs] = blocks[i * bw + j]

    jj += 1
    if jj >= bw:
        jj = 0
        ii += 1

plt.imshow(nimg, cmap='gray')
plt.show()