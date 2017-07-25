# -*- coding:utf-8 -*-

def LCG(k, c, m, seed):
    x = seed
    while True:
        yield x
        x = (k * x + c) % m
    
lcg = LCG(19, 51, 100, 25)

for x in lcg:
    print (x)
