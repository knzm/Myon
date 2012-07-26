#! /usr/bin/python
# -*- coding:utf-8 -*-

from Kuin import *

class Eval(object):
    def __init__(self):
        self.ops = [x[0] for x in Operators]
        self.lexis = [[u"var", u"int", 0, u"i", 10]]

    def execute(self, _token):
        prior = MAX_OPRI
        _out = []
        _stack = [[]]
        _braket = 0
        for i in range(len(_token)):
            if _token[i].isdigit():
                _out.append(_token[i])
            elif _token[i] in [x[3] for x in self.lexis]:
                _out.append(_token[i])
            elif _token[i] == u'(':
                _braket += 1
                _stack.append([])
            elif _token[i] == u')':
                _braket -= 1
                _out += _stack[-1][::-1]
                _stack.pop()
            elif _token[i] in self.ops:
                _prior = Operators[self.ops.index(_token[i])][1]
                if _prior < prior+_braket*MAX_OPRI:
                    _stack[-1].append(_token[i])
                else:
                    _out.append(_stack[-1][::-1])
                    _stack[-1] = [_token[i]]
                prior = _prior
            else:
                print u"SyntaxError:不明なトークンです\n",_token[i]
        return _out

class Lexer(object):
    def __init__(self):
        self.lexis = []
        self.index = -1
        self.eval = Eval()
        self.eval.execute(list(u"5^((1*3)^(2*5))"))
    
    def newlex(self, *_token):
        self.lexis.append(*_token)
        self.index += 1

    def replex(self, _index, _value):
        self.lexis[self.index][_index] = _value

    def analylex(self, _token):
# print "token:", _token
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
# print param
                        # check if the value is defined and calculate
# else: print u"SyntaxError: for()の括弧内は数値のみです><\n"+_token[i]
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
# print param
                        # check if the value is defined and calculate
# else: print u"SyntaxError: for()の括弧内は数値のみです><\n"+_token[i]
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

