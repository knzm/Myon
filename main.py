#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys

from Kuin import *

def orsplit(_str, *signs):
    _out = []
    _idx = 0
    for i in range(len(_str)):
        if _str[i] in signs:
            _out.append(_str[_idx:i])
            _out.append(_str[i])
            _idx = i+1
    _out.append(_str[_idx:])
    return _out

class Parse(object):
    def __init__(self):
        self.index = -1
        self.reindex = -1
        self.depth = 0
        self.token = []
        self.mode = "block_start"
        self.premode = "None"

    def newtoken(self, _block, _token):
        self.token.append([self.depth, _block, False, _token])
        self.index += 1
        self.reindex = self.index

        if _block.split("_")[0] == "block":
            self.depth += 1

    def addtoken(self, _token):
        self.token[self.index].append(_token)

    def gettoken(self, _code):
        _code = _code.split(u" ")
        code = []
        for i in range(len(_code)):
            _list = orsplit(_code[i], u"\n", *Signs)
            for x in _list:
                code.append(x)

        for i in range(len(code)):
            if code[i] in [u"", u"\n"]: continue
            if code[i] == u"{":
                self.premode = self.mode
                self.mode = "comment"

            if self.mode == "comment":
                if code[i] == u"}":
                    self.mode = self.premode

            elif self.mode == "block_start":
                if code[i] in [u"func", u"for", u"if"]:
                    self.mode = "block_name"
                    self.block = code[i]
                elif code[i] in [u"end"]:
                    self.mode = "block_return"
                else:
                    self.mode = "state"

                if self.mode != "block_return": self.newtoken(self.mode, code[i])

            elif self.mode == "block_name":
                if u"(" in code[i] and u")" in code[i]:
                    self.mode = "state_end"
                if u"(" in code[i]:
                    self.addtoken(code[i])
                elif u")" in code[i]:
                    if not code[i] in self.token[self.index]: self.addtoken(code[i])
                    self.mode = "state_end"
                else:
                    self.addtoken(code[i])

            elif self.mode == "block_return":
                if self.reindex == 0 and self.token[self.reindex][2] == True:
                    print u"ParseError: ！！！突然のendブロック！！！\n"+code[i]

                idx = 0
                for j in range(self.reindex):
                    if self.token[self.reindex-j][1] == "block_name" and self.token[self.reindex-j][2] == False:
                        idx = self.reindex-j
                        break
                if code[i] != self.token[idx][3]:
                    print u"ParseError:"+self.token[idx][3]+u" ブロックがちゃんと閉じられていませんみょん><\n"+code[i]
                    print idx,self.reindex
                else:
                    self.reindex = idx-1
                    if self.reindex<0: self.reindex = 0
                    self.depth -= 1
                    self.token[idx][2] = True

            elif self.mode == "state":
                self.addtoken(code[i])

            elif self.mode in ["state_end", "state", "block_start"]:
                print u"ParseError: 1行に2つ以上の命令を書かないでくださいみょん><\n"+code[i]

        if self.mode in ["state_end", "state", "block_return", "block_start"]:
            self.mode = "block_start"
        else:
            print u"ParseError: 不明なエラー\n"+self.mode

    def putcode(self, fname):
        _fname = "".join(fname.split(".")[:-1])+".py"
#        _fline = open(_fname, 'w')
#        _fline.write(u"#! /usr/bin/python".encode('utf-8'))
#        _fline.write(u"# -*- coding:utf-8 -*-".encode('utf-8'))

        _pyline = u""
        for i in range(len(self.token)):
            _pyline += u" "*4*self.token[i][0]

            # replace token-list
                
#            _fline.write(_pyline+"\n").encode('utf-8'))

            print self.token[i]

#        _fline.close()
        print "...compile done... -> "+_fname

class Myon(object):
    def __init__(self, filename):
        self.fname = filename
        self.fline = open(self.fname, 'r')
        self.pline = self.fline.readline().decode('utf-8')
        self.parse = Parse()

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
