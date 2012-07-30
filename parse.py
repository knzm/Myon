#! /usr/bin/python
# -*- coding:utf-8 -*-

import lexer
from Kuin import *

def orsplit(_str):
    mode, premode = '', ''
    _token = []
    _index = -1
    for i in range(len(_str)):
        if _str[i] in [u":", u"+", u"-", u"*", u"/", u"%", u"^", u"~"]:
            mode = 'signs_14'
        elif _str[i] in [u"<", u">", u"="]:
            mode = 'signs_10'
        elif _str[i] in [u".", u"!", u"&", u"|", u"?"]:
            mode = 'signs'
        elif _str[i] in [u"(", u")", u"[", u"]"]:
            mode = 'brakets'+_str[i]
        elif _str[i] == u'\n':
            mode = '\n'
        elif _str[i].isalnum() or _str[i] == u"@":
            mode = 'alnum'
        else:
            mode = 'other'

        if mode != premode:
            _token.append(_str[i])
            _index += 1
        else:
            _token[_index]+=_str[i]

        premode = mode
    return _token

class Parse(object):
    def __init__(self):
        self.index = -1
        self.reindex = -1
        self.depth = 0
        self.token = []
        self.mode = "block_start"
        self.premode = "None"

        self.lexer = lexer.Lexer()

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
            _list = orsplit(_code[i])
            for x in _list:
                code.append(x)
# print "code:", code

        for i in range(len(code)):
            if code[i] == u"\n": continue
            if code[i] == u"{":
                self.premode = self.mode
                self.mode = "comment"

            if self.mode == "comment":
                if code[i] == u"}":
                    self.mode = self.premode

            elif self.mode == "block_start":
                if code[i] in [u"func", u"for", u"if"]:
                    self.mode = "block_name"
                elif code[i] in [u"end"]:
                    self.mode = "block_return"
                else:
                    self.mode = "state"

                if self.mode != "block_return": self.newtoken(self.mode, code[i])

            elif self.mode == "block_name":
                if u"(" == code[i]:
                    self.mode = "state_start"
                else:
                    pass
                self.addtoken(code[i])

            elif self.mode == "block_return":
                if self.reindex == 0 and self.token[self.reindex][2] == True:
                    print u"BlockError: ！！！突然のendブロック！！！\n"+code[i]

                idx = 0
                for j in range(self.reindex):
                    if self.token[self.reindex-j][1] == "block_name" and self.token[self.reindex-j][2] == False:
                        idx = self.reindex-j
                        break
                if code[i] != self.token[idx][3]:
                    print u"BlockError:"+self.token[idx][3]+u" ブロックがちゃんと閉じられていませんみょん><\n"+code[i]
                    print idx,self.reindex
                else:
                    self.reindex = idx-1
                    if self.reindex<0: self.reindex = 0
                    self.depth -= 1
                    self.token[idx][2] = True

            elif self.mode == "state":
                self.addtoken(code[i])

            elif self.mode == "state_start":
                self.addtoken(code[i])
                if code[i] == u")":
                    self.mode = "block_return"
            else:
                print u"BlockError: 1行に2つ以上の命令を書かないでくださいみょん><\n"+code[i]

        if self.mode in ["state_end", "state", "block_return", "block_start"]:
            self.mode = "block_start"
        elif self.mode == "state_start":
            print self.block+u"文は2行にまたがることはできませんみょん><"
        else:
            print u"BlockError: 不明なエラー\n"+self.mode

        return self.token

    def putcode(self, fname):
        for i in range(len(self.token)):
            self.token[i] = self.lexer.analylex(self.token[i])

        _pyline = u""
        for i in range(len(self.token)):
            _pyline += u" "*4*self.token[i][0]+self.token[i][3]+u"\n"

        _fname = "".join(fname.split(".")[:-1])+".py"
        _fline = open(_fname, 'w')
        _fline.write(u"#! /usr/bin/python\n".encode('utf-8'))
        _fline.write(u"# -*- coding:utf-8 -*-\n".encode('utf-8'))
        _fline.write(_pyline.encode('utf-8'))
        _fline.write(u'if __name__ == "__main__":\n Main()'.encode('utf-8'))
        _fline.close()

        print "...compile done... -> "+_fname

    def putline(self):
        for i in range(len(self.token)):
            self.token[i] = self.lexer.analylex(self.token[i])

        _pyline = u""
        for i in range(len(self.token)):
            _pyline += u" "*4*self.token[i][0]+self.token[i][3]+u"\n"

        return _pyline

