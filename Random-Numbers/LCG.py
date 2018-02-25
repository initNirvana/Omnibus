# -*- coding:utf-8 -*-

def LCG(k, c, m, seed):
    x = seed
    while True:
        yield x
        x = (k * x + c) % m

def LCG2(r, x, seed):
    x = seed
    while True:
        yield x
        x = r * x * (1 - x)

#lcg = LCG(19, 51, 100, 25)
lcg = LCG2(4, 0.5, 0.8)

for x in lcg:
    print (x)
