#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys
import parse

from Kuin import *

class Myon(object):
    def __init__(self, filename):
        self.parse = parse.Parse()
        self.fname = filename

    def loadfile(self,filename):
        self.parse.index = -1
        self.parse.reindex = -1

        self.parse.token = []
        self.parse.premode = "None"
        self.parse.exflag = "False"

        self.parse.lexer.eval.setfile(filename)

        self.fline = open(filename, 'r')
        self.pline = self.fline.readline().decode('utf-8')
        while self.pline != u"":
            self.pline = self.fline.readline().decode('utf-8')
            if self.parse.gettoken(self.pline, self.fname, filename) == -1: return -1
        self.fline.close()

    def main(self):
        self.loadfile(self.fname)
        self.parse.checkerror()
        self.parse.putcode(self.fname, mode="main")

        path = u"/".join(self.fname.split(u"/")[:-1])+u"/"
        for current_file in self.parse.fname:
            self.loadfile(path+current_file)
            self.parse.putcode(path+current_file)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print u"Error: E0002 ソースコードを一つだけ食べさせてください。例：kuin.exe hoge.kn"
    else:
        if sys.argv[-1].split(".")[-1] != "kn":
            print "Error: E0005 ソースコードのファイル形式が不明です。.knファイルを食べさせてください。"
        myon = Myon(sys.argv[1].decode('utf-8'))
        myon.main()
