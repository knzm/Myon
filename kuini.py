#! /usr/bin/python
# -*- coding:utf-8 -*-

import evals
from Kuin import *

class Interpreter(object):
    def __init__(self):
        self.eval = evals.Eval()
    
    def exe(self, _str):
        return self.eval.execute(_str)

if __name__=="__main__":
    kuini = Interpreter()

    s = ""
    while True:
        s = raw_input(">")
        if s=="quit": break

        print eval(kuini.exe(s))
