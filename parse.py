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
            mode = 'brakets'+str(i)
        elif _str[i] == u'\n':
            mode = '\n'
        elif _str[i].isalnum() or _str[i] == u"@" or _str[i] == u"_":
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
        self.blockIndex = [[0,0]]

        self.token = []
        self.mode = "block_start"
        self.premode = "None"

        self.lexer = lexer.Lexer()

        self.fname = []
        self.excompile = []
        self.exflag = False

    def newtoken(self, _block, _token):
        self.token.append([str(self.depth)+u"_"+str(self.blockIndex[self.depth][1]), _block, False, _token])
        self.index += 1
        self.reindex = self.index

        if _block.split("_")[0] == "block":
            self.depth += 1
            self.blockIndex.append([self.depth, 0])

    def addtoken(self, _token):
        self.token[self.index].append(_token)

    def gettoken(self, _code, fname, current_fname):
        if fname != current_fname:
            _fname = current_fname.split("/")[-1].split(".")[0]
            for i in range(len(self.lexer.eval.excompile)):
                if self.lexer.eval.excompile[i][0] == _fname:
                    self.excompile = [self.lexer.eval.excompile[i][1]]

        _code = _code.split(u" ")
        code = []
        for i in range(len(_code)):
            _list = orsplit(_code[i])
            for x in _list:
                code.append(x)

        for i in range(len(code)):
            if fname != current_fname:
                if code[i] == u"func" and code[i+1] in self.excompile:
                    self.exflag = True

                if self.exflag == False:
                    break

            if self.mode != "__python__" and code[i] == u"\n": continue
            if code[i] == u"{":
                self.premode = self.mode
                self.mode = "comment"
            
            if self.mode == "comment":
                if code[i] == u"}":
                    self.mode = self.premode

            elif self.mode == "block_start":
                if code[i] in [u"func", u"for", u"if"]:
                    self.mode = "block_name"
                    self.newtoken(self.mode, code[i])
                elif code[i] in [u"__python__"]:
                    self.mode = "__python__"
                elif code[i] in [u"import"]:
                    self.mode = "import"
                    self.newtoken(self.mode, code[i])
                elif code[i] in [u"end"]:
                    self.mode = "block_return"
                else:
                    self.mode = "state"
                    self.newtoken(self.mode, code[i])

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
                    print u"Error: E0014 ブロックを閉じ忘れています。end文 でちゃんと閉じましょう。\n",self.fname,code[i],self.token[idx][3]
                    print idx,self.reindex
                else:
                    self.reindex = idx-1
                    if self.reindex<0: self.reindex = 0
                    self.blockIndex[self.depth][1] += 1
                    self.depth -= 1
                    self.token[idx][2] = True

                    if fname != current_fname:
                        self.exflag = False

            elif self.mode == "state":
                self.addtoken(code[i])

            elif self.mode == "state_start":
                self.addtoken(code[i])
                if code[i] == u")":
                    self.mode = "block_return"

            elif self.mode == "__python__":
                if code[i] == u"__end_python__":
                    self.mode = "block_start"
                else:
                    if code[i] == u"__python__":
                        print u"Warning: W0000 '__python__'を入れ子にすることはできません。\n"
                    elif i == 0:
                        self.newtoken(self.mode, u"__python__")
                        self.addtoken(" ".join(_code).strip())

            elif self.mode == "import":
                self.fname.append(code[i]+u".kn")
                self.addtoken(code[i])
                self.mode = "block_start"

            else:
                print u"BlockError: 1行に2つ以上の命令を書かないでくださいみょん><\n"+code[i]

            if code[i] == u"func":
                self.lexer.eval.newlex([u"func", u"void", u"", code[i+1]])

        if self.mode in ["state_end", "state", "block_return", "block_start"]:
            self.mode = "block_start"
        elif self.mode == "state_start":
            print self.block+u"文は2行にまたがることはできませんみょん><"
        elif self.mode == "__python__":
            pass
        else:
            print u"Error: E0008 構文エラーです。ドキュメントを参照し、正しい文法になっているか確認してください。"+self.mode

        return self.token

    def putcode(self, fname, mode="extern"):
        if mode == "main":
            for i in range(len(self.token)):
                self.token[i] = self.lexer.analylex(self.token[i])

            _pyline = u""
            for i in range(len(self.token)):
                _pyline += u" "*4*int(self.token[i][0].split("_")[0])+self.token[i][3]+u"\n"

        else:
            for i in range(len(self.token)):
                self.token[i] = self.lexer.analylex(self.token[i])

            _pyline = u""
            for i in range(len(self.token)):
                _pyline += u" "*4*int(self.token[i][0].split("_")[0])+self.token[i][3]+u"\n"

#            for i in range(len(excompile)):
#                if excompile[i][0] == fname.split(u"/")[-1].split(u".")[0]:
#                    print excompile[i][0]
#                    print self.token

        _fname = "".join(fname.split(".")[:-1])+".py"
        _fline = open(_fname, 'w')
        _fline.write(u"#! /usr/bin/python\n".encode('utf-8'))
        _fline.write(u"# -*- coding:utf-8 -*-\n".encode('utf-8'))
        _fline.write(_pyline.encode('utf-8'))
        _fline.write(u'if __name__ == "__main__":\n    Main()'.encode('utf-8'))
        _fline.close()

        print "...compile done... -> "+_fname

    def putline(self):
        for i in range(len(self.token)):
            self.token[i] = self.lexer.analylex(self.token[i])

        _pyline = u""
        for i in range(len(self.token)):
            _pyline += u" "*4*self.token[i][0]+self.token[i][3]+u"\n"

        return _pyline

    def checkerror(self):
        if not u"Main" in [x[4] for x in self.token]:
            print u"Warning: W0001 Main関数がありません。意図されたプログラムですか？"
        
        if self.mode == "__python__":
            print u"Caution: C0001 __python__ブロックを閉じ忘れています。__end_python__でちゃんと閉じましょう。"

        for i in range(len(self.token)):
            if self.token[i][1] == "block_name" and self.token[i][2] == False:
                print u"Cartion: C0002 "+self.token[i][3]+u"ブロックを閉じ忘れています。end文でちゃんと閉じましょう。"

        return


