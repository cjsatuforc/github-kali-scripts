#!/usr/bin/env python
#Tool for brute forcing pin codes that are a static length
import sys
from rflib import *
from struct import *
import argparse

parser = argparse.ArgumentParser(description='Calculate all permutations of a specified character set and specified length. Usage: python pinbrute.py -c \'0123456789\' -l 3',version="0")
parser.add_argument('-c', action="store", dest="characters",default='0123456789',help='Character set: 01, 0123456789, +*#, ABCDEFG',type=str)
parser.add_argument('-l', action="store", dest="fixedlength",default=3,help='Fixed Length of Pincode/Password',type=int)
parser.add_argument('-p', action="store", dest="prepend",default='',help='Prepend static characters before pin',type=str)
parser.add_argument('-t', action="store", dest="append",default='',help='Append static characters after pin',type=str)
args = parser.parse_args()

##### de Bruijn Sequence borrowed from Peter Otten - http://code.activestate.com/lists/python-list/660415/ #####
_mapping = bytearray(b"?")*256
_mapping[:len(args.characters)] = args.characters

def debruijn_bytes(k, n):
    a = k * n * bytearray([0])
    sequence = bytearray()
    extend = sequence.extend
    def db(t, p):
        if t > n:
            if n % p == 0:
                extend(a[1: p+1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    db(1, 1)
    return sequence.translate(_mapping).decode("ascii")
##### end of borrowed code #####

seq = debruijn_bytes(len(args.characters), args.fixedlength)
tail = seq[:args.fixedlength-1]
debruijn = (seq+tail)

startn = 0
endy = args.fixedlength
while(startn < len(debruijn)-(args.fixedlength-1)):
   print(args.prepend+debruijn[startn:endy]+args.append)
   startn = startn + 1
   endy = endy + 1