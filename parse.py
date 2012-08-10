# -*- coding:utf-8 -*-

import os

import lexer
from Kuin import *


def orsplit(_str):
    mode, premode = '', ''
    _token = []
    _index = -1
    for i, char in enumerate(_str):
        if char in u":+-*/%^~":
            mode = 'signs_14'
        elif char in u"<>=":
            mode = 'signs_10'
        elif char in u".!&|?":
            mode = 'signs'
        elif char in u"()[]":
            mode = 'brakets%d' % i
        elif char == u'\n':
            mode = '\n'
        elif char.isalnum() or char in u"@_\"'":
            mode = 'alnum'
        else:
            mode = 'other'

        if mode != premode:
            _token.append(char)
            _index += 1
        else:
            _token[_index] += char

        premode = mode
    return _token


class Parse(object):
    def __init__(self):
        self.index = -1
        self.reindex = -1

        self.depth = 0
        self.blockIndex = [[0, 0]]

        self.token = []
        self.mode = "block_start"
        self.premode = "None"

        self.lexer = lexer.Lexer()

        self.fname = []
        self.excompile = []
        self.exflag = False

        self.comment = 0

    def newtoken(self, _block, _token):
        loc = "_".join([str(self.depth), str(self.blockIndex[self.depth][1])])
        self.token.append([loc, _block, False, _token])
        self.index += 1
        self.reindex = self.index

        if _block.split("_")[0] == "block":
            self.depth += 1
            self.blockIndex.append([self.depth, 0])

    def addtoken(self, _token):
        self.token[self.index].append(_token)

    def gettoken(self, _code, fname, current_fname):
        if fname != current_fname:
            _fname = os.path.splitext(os.path.basename(current_fname))[0]
            for i, x in enumerate(self.lexer.eval.excompile):
                if x[0] == _fname:
                    self.excompile = [x[1]]

        tokens = []
        for c in _code.split(u" "):
            tokens += orsplit(c)

        for i, current_token in enumerate(tokens):
            if fname != current_fname:
                if current_token == u"func" and tokens[i+1] in self.excompile:
                    self.exflag = True
                if not self.exflag:
                    break

            if self.mode not in ["__python__", "state_start"] and \
                    current_token == u"\n":
                continue

            if current_token == u"{":
                if self.mode != "comment":
                    self.premode = self.mode
                self.mode = "comment"
                self.comment += 1

            if self.mode == "comment":
                if current_token == u"}":
                    self.comment -= 1
                if self.comment == 0:
                    self.mode = self.premode

            elif self.mode == "block_start":
                if current_token in [u"func", u"for", u"if"]:
                    self.mode = "block_name"
                    self.newtoken(self.mode, current_token)
                elif current_token in [u"__python__"]:
                    self.mode = "__python__"
                elif current_token in [u"import"]:
                    self.mode = "import"
                    self.newtoken(self.mode, current_token)
                elif current_token in [u"end"]:
                    self.mode = "block_return"
                else:
                    self.mode = "state"
                    self.newtoken(self.mode, current_token)

            elif self.mode == "block_name":
                if current_token == u"(":
                    self.mode = "state_start"
                else:
                    pass
                self.addtoken(current_token)

            elif self.mode == "block_return":
                if self.reindex == 0 and self.token[self.reindex][2]:
                    print u"BlockError: ！！！突然のendブロック！！！\n", current_token

                idx = 0
                for k in range(self.reindex, 0, -1):
                    if self.token[k][1] == "block_name" and \
                            not self.token[k][2]:
                        idx = k
                        break
                if current_token != self.token[idx][3]:
                    print u"Error: E0014 ブロックを閉じ忘れています。end文 でちゃんと閉じましょう。\n", self.fname, current_token, self.token[idx][3]
                    print idx, self.reindex
                else:
                    self.reindex = idx - 1
                    if self.reindex < 0:
                        self.reindex = 0
                    self.blockIndex[self.depth][1] += 1
                    self.depth -= 1
                    self.token[idx][2] = True

                    if fname != current_fname:
                        self.exflag = False

            elif self.mode == "state":
                self.addtoken(current_token)

                if self.token[self.index][3] == u"return":
                    for i in reversed(range(self.index)):
                        if self.token[i][3] == u"func" and \
                                not self.token[i][2]:
                            names = [x[4] for x in self.lexer.eval.elements]
                            _idx = names.index(self.token[i][4])
                    self.token[self.index][2] = \
                        self.lexer.eval.elements[_idx][2]

            elif self.mode == "state_start":
                if current_token == u'\n':
                    self.mode = "block_return"
                else:
                    self.addtoken(current_token)

            elif self.mode == "__python__":
                if current_token == u"__end_python__":
                    self.mode = "block_start"
                else:
                    if current_token == u"__python__":
                        print u"Warning: W0000 '__python__'を入れ子にすることはできません。\n"
                    elif i == 0:
                        self.newtoken(self.mode, u"__python__")
                        self.addtoken(_code)

            elif self.mode == "import":
                self.fname.append(current_token + u".kn")
                self.addtoken(current_token)
                self.mode = "block_start"

            else:
                print u"BlockError: 1行に2つ以上の命令を書かないでくださいみょん><\n", current_token

            if self.mode == "block_return" and \
                    u"func" in tokens and tokens[0] != u"end":
                t = self.token[self.index]
                args = self.lexer.analylex(t, True)[5]
                t[5] = args
                if args != [[]]:
                    loc = u"_".join([str(self.depth),
                                     str(self.blockIndex[self.depth][1])])
                    for var_name, var_type in args:
                        self.lexer.eval.newlex(
                            [u"var", var_type, loc, var_name])

        if self.mode in ["state_end", "state", "block_return", "block_start"]:
            self.mode = "block_start"
        elif self.mode == "state_start":
            print u"文は2行にまたがることはできませんみょん><", current_token
        elif self.mode == "__python__":
            pass
        else:
            print u"Error: E0008 構文エラーです。ドキュメントを参照し、正しい文法になっているか確認してください。", self.mode

        return self.token

    def putline(self):
        self.token = [self.lexer.analylex(t) for t in self.token]

        pylines = []
        for token in self.token:
            depth = 4 * token[0]
            pylines.append(u" " * depth + token[3])

        return "".join([line + "\n" for line in pylines])

    def getcode(self, fname, mode="extern"):
        if mode == "main":
            self.token = [self.lexer.analylex(t) for t in self.token]

            pylines = []
            for token in self.token:
                depth = 4 * int(token[0].split("_")[0])
                pylines.append(u" " * depth + token[3])

        else:
            self.token = [self.lexer.analylex(t) for t in self.token]

            pylines = []
            for token in self.token:
                depth = 4 * int(token[0].split("_")[0])
                pylines.append(u" " * depth + token[3])

            # _name = os.path.splitext(os.path.basename(fname))[0]
            # for i, x in enumerate(excompile):
            #     if x[0] == _name:
            #         print x[0]
            #         print self.token

        return "".join([line + "\n" for line in pylines])

    def putcode(self, fname, mode="extern"):
        code = self.getcode(fname, mode=mode)
        out_name = os.path.splitext(fname)[0] + ".py"
        with open(out_name, 'w') as out:
            out.write("#! /usr/bin/python\n")
            out.write("# -*- coding:utf-8 -*-\n")
            out.write(code.encode('utf-8'))
            out.write('if __name__ == "__main__":\n')
            out.write('    Main()\n')
        print "...compile done... -> " + out_name

    def checkerror(self, isMain=False):
        if isMain and u"Main" not in [x[4] for x in self.token]:
            print u"Warning: W0001 Main関数がありません。意図されたプログラムですか？"

        if self.mode == "__python__":
            print u"Caution: C0001 __python__ブロックを閉じ忘れています。__end_python__でちゃんと閉じましょう。"

        for token in self.token:
            if token[1] == "block_name" and not token[2]:
                print u"Cartion: C0002 %sブロックを閉じ忘れています。end文でちゃんと閉じましょう。" % token[3]

    def checkfunc(self):
        for excompile in self.lexer.eval.excompile:
            isFound = False
            for element in self.lexer.eval.elements:
                if (element[0], element[4]) == (excompile[0], excompile[1]):
                    isFound = True
            if not isFound:
                print u"Error: E0025 未定義の識別子です。タイプミスに気をつけ、正しい名前を指定してください。\n", excompile
