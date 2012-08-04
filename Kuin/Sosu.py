#! /usr/bin/python
# -*- coding:utf-8 -*-
import Log
def Main():
    for i in range(2, 100):
        b = bool(False)
        for j in range(2, (i-1)):
            if ((i%j)==0):
                b = True
        if not b:
            Log.WriteLn(i)
if __name__ == "__main__":
    Main()