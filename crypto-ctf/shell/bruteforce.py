p = 751672198763
g = 70600674451
A = 518295907282

for a in range(1, p):
    if pow(g, a, p) == A:
        break

print(a)