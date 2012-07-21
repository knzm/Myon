#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys
import re

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

class Lexer(object):
    def __init__(self):
        self.lexis = []
        self.index = -1
    
    def newlex(self, *_token):
        self.lexis.append(*_token)
        self.index += 1

    def replex(self, _index, _value):
        self.lexis[self.index][_index] = _value

    def analylex(self, _token):
#        print "token:", _token
        if _token[3] == u"func":
            _token[3] = u"def"
            self.newlex([u"func", u"void", _token[0], _token[4]])
            # set some parameters

            _token[3] += u" "+u"".join(_token[4:])+u":"
        elif _token[3] == u"for":
            self.newlex([u"var", u"int", _token[0], _token[4]])
            
            mode, param, index = "(", [u""], 0
            for i in range(len(_token)):
                if mode == "(":
                    if _token[i] == u"(":
                        mode = "param"
                elif mode == "param":
                    if _token[i] == u",":
                        param.append(u"")
                        index += 1
                    elif _token[i] == u")": mode = u")"
                    else:
                        param[index] += _token[i]
#                        print param
                        # check if the value is defined and calculate
#                        else: print u"SyntaxError: for()の括弧内は数値のみです><\n"+_token[i]
                elif mode == ")":
                    if len(param) in [2, 3]: break
                    else: print u"SyntaxError: for()の中のパラメータの数がおかしいです><"

            _token[3] += u" "+_token[4] + u" in range("+str(", ".join(param))+u"):"
            _token[5:] = ""

        elif _token[3] == u"if":
            mode, param, index = "(", [u""], 0
            for i in range(len(_token)):
                if mode == "(":
                    if _token[i] == u"(":
                        mode = "param"
                elif mode == "param":
                    if _token[i] == u")": mode = u")"
                    else:
                        param[index] += _token[i]
#                        print param
                        # check if the value is defined and calculate
#                        else: print u"SyntaxError: for()の括弧内は数値のみです><\n"+_token[i]
                elif mode == ")":
                    if len(param) in [2, 3]: break
                    else: print u"SyntaxError: for()の中のパラメータの数がおかしいです><"

            _token[3] += u" "+str(", ".join(param))+u":"

            # calculate
            if len(_token[3].split("="))!=1: _token[3] = u"==".join(_token[3].split("="))
            if len(_token[3].split("!"))!=1: _token[3] = u"not ".join(_token[3].split("!"))

        elif _token[3] == u"var":
            mode = "var"
            for i in range(len(_token)):
                if mode == "var":
                    if _token[i] == u"var":
                        mode = "name"
                elif mode == "name":
                    self.newlex([u"var", u"", _token[0], _token[i], None])
                    mode = ":"
                elif mode == ":":
                    if _token[i] == u":": mode = "type"
                    else: print u"SyntaxError: :による変数の宣言が不正です><\n"+str(_token[i])
                elif mode == "type":
                    if _token[i] in Types:
                        self.replex(1, _token[i])
                        mode = "::"
                    else:
                        print u"SytaxError: 存在しない型です><\n"+_token[i]
                elif mode == "::":
                    if _token[i] == u"::": mode = "attr"
                    else: print u"SyntaxError: ::による変数の代入が不正です><\n"+str(_token[i])
                elif mode == "attr":
                    if self.lexis[self.index][1] == u"bool":
                        if _token[i] == u"false": _token[i] = u"False"
                        else: _token[i] = u"True"
                    self.replex(4, _token[i])
                else: print u"不明なえらー\n"+str(_token[i])

            if not mode in ["type", "attr"]:
                print u"SyntaxError: varの宣言が不正です><\n"+_token[i]

            if mode == "attr":
                _this = self.lexis[self.index]
                _token[3] = _this[3]+u" = "+_this[1]+u"("+_this[4]+")"

        elif _token[3] == u"do":
            mode = "do"
            _index = 0
            for i in range(len(_token)):
                if mode == "do":
                    if _token[i] == u"do": mode = "name"                    
                elif mode == "name":
                    if _token[i] in [x[3] for x in self.lexis]:
                        _index = [x[3] for x in self.lexis].index(_token[i])
                        mode = "::"
                    elif _token[i] == u"Log@WriteLn":
                        mode = "function"
                    else:
                        print u"SyntaxError: 存在しない変数または関数です><\n"+_token[i]
                elif mode == "::":
                    if _token[i] == u"::": mode = "attr"
                    else: print u"SyntaxError: ::による変数の代入が不正です><\n"+str(_token[i])
                elif mode == "attr":
                    if self.lexis[_index][1] == u"bool":
                        if _token[i] == u"false": _token[i] = u"False"
                        else: _token[i] = u"True"
                    self.lexis[_index][4] = _token[i]
                elif mode == "function":
                    pass
                else: print u"不明なえらー\n"+mode

            if not mode in ["type", "attr", "function"]:
                print u"SyntaxError: varの宣言が不正です><\n"+_token[i]

            if mode == "attr":
                _this = self.lexis[_index]
                _token[3] = _this[3]+u" = "+_this[4]

            if mode == "function":
                if _token[4] == u"Log@WriteLn":
                    _token[3] = u"print "+_token[6]            

        return _token

class Parse(object):
    def __init__(self):
        self.index = -1
        self.reindex = -1
        self.depth = 0
        self.token = []
        self.mode = "block_start"
        self.premode = "None"

        self.lexer = Lexer()

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
#        print "code:", code

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
        _fline.write(u'if __name__ == "__main__":\n    Main()'.encode('utf-8'))
        _fline.close()

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
