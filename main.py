#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys
import parse

from Kuin import *

class Myon(object):
    def __init__(self, filename):
        self.fname = filename
        self.fline = open(self.fname, 'r')
        self.pline = self.fline.readline().decode('utf-8')
        self.parse = parse.Parse()

    def main(self):
        while self.pline != u"":
            self.pline = self.fline.readline().decode('utf-8')
            if self.parse.gettoken(self.pline) == -1: return -1
        
        self.parse.putcode(self.fname)

if __name__ == "__main__":
    if len(sys.argv) == 1: print u"CompileError: ファイルがありませんみょん><"
    else:
        myon = Myon(sys.argv[1])
        myon.main()
