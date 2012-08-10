#! /usr/bin/python
# -*- coding:utf-8 -*-

import evals
import parse
import lexer
from Kuin import *


class Interpreter(object):
    def __init__(self):
        self.eval = evals.Eval()
        self.parse = parse.Parse()
        self.lexer = lexer.Lexer()

    def exe(self, _str):
        return self.eval.execute(_str)


if __name__=="__main__":
    kuini = Interpreter()

    s = ""
    while True:
        s = raw_input(">")
        if s == "quit":
            break

        kuini.parse.__init__()
        print kuini.parse.gettoken(s, "", "")[0]
        print eval(kuini.eval.execute(kuini.parse.gettoken(s, "", "")[0][3:], u"0_0"))
