#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys

class Parse(object):
    def __init__(self):
        self.index = 0
        self.element = []
        self.mode = "any"

    def analy(self, _list):
        print _list
        self.index += 1

class Myon(object):
    def __init__(self, filename):
        self.fname = filename
        self.fline = open(self.fname, 'r')
        self.pline = ""
        self.parse = Parse()

    def main(self):
        while self.parse.index == 0 or self.pline != "":
            self.pline = self.fline.readline().decode('utf-8')
            self.parse.analy(self.pline.split(u' '))

if __name__ == "__main__":
    if len(sys.argv) == 1: print u"CompileError: ファイルがありませんみょん><"
    else:
        myon = Myon(sys.argv[1])
        myon.main()
