#! /usr/bin/python
# -*- coding:utf-8 -*-
def Main():
    for i in range(2, 100):
        b = bool(False)
        for j in range(2, i-1):
            if i%j==0:
                b = True
        if not b:
            print i
if __name__ == "__main__":
    Main()