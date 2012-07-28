#! /usr/bin/python
# -*- coding:utf-8 -*-

from Kuin import *
import evals

class Lexer(object):
    def __init__(self):
        self.lexis = []
        self.index = -1
        self.eval = evals.Eval()
    
    def analylex(self, _token):
# print "token:", _token
        if _token[3] == u"func":
            _token[3] = u"def"
            self.eval.newlex([u"func", u"void", _token[0], _token[4]])
            # set some parameters
            _token[3] += u" "+u"".join(_token[4:])+u":"
        elif _token[3] == u"for":
            self.eval.newlex([u"var", u"int", _token[0], _token[4]])
            
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
                    self.eval.newlex([u"var", u"", _token[0], _token[i], None])
                    mode = ":"
                elif mode == ":":
                    if _token[i] == u":": mode = "type"
                    else: print u"SyntaxError: :による変数の宣言が不正です><\n"+str(_token[i])
                elif mode == "type":
                    if _token[i] in Types:
                        self.eval.replex(1, _token[i])
                        mode = "::"
                    else:
                        print u"SytaxError: 存在しない型です><\n"+_token[i]
                elif mode == "::":
                    if _token[i] == u"::": mode = "attr"
                    else: print u"SyntaxError: ::による変数の代入が不正です><\n"+str(_token[i])
                elif mode == "attr":
                    if self.eval.elements[self.index][1] == u"bool":
                        if _token[i] == u"false": _token[i] = u"False"
                        else: _token[i] = u"True"
                    self.eval.replex(4, _token[i])
                else: print u"不明なえらー\n"+str(_token[i])

            if not mode in ["type", "attr"]:
                print u"SyntaxError: varの宣言が不正です><\n"+_token[i]

            if mode == "attr":
                _this = self.eval.elements[self.index]
                _token[3] = _this[3]+u" = "+_this[1]+u"("+_this[4]+")"

        elif _token[3] == u"do":
            mode = "do"
            _index = 0
            for i in range(len(_token)):
                if mode == "do":
                    if _token[i] == u"do": mode = "name"
                elif mode == "name":
                    if _token[i] in [x[3] for x in self.eval.elements]:
                        _index = [x[3] for x in self.eval.elements].index(_token[i])
                        mode = "::"
                    elif _token[i] == u"Log@WriteLn":
                        mode = "function"
                    else:
                        print u"SyntaxError: 存在しない変数または関数です><\n"+_token[i]
                elif mode == "::":
                    if _token[i] == u"::": mode = "attr"
                    else: print u"SyntaxError: ::による変数の代入が不正です><\n"+str(_token[i])
                elif mode == "attr":
                    if self.eval.elements[_index][1] == u"bool":
                        if _token[i] == u"false": _token[i] = u"False"
                        else: _token[i] = u"True"
                    self.eval.elements[_index][4] = _token[i]
                elif mode == "function":
                    pass
                else: print u"不明なえらー\n"+mode

            if not mode in ["type", "attr", "function"]:
                print u"SyntaxError: varの宣言が不正です><\n"+_token[i]

            if mode == "attr":
                _this = self.eval.elements[_index]
                _token[3] = _this[3]+u" = "+_this[4]

            if mode == "function":
                if _token[4] == u"Log@WriteLn":
                    _token[3] = u"print "+_token[6]

        return _token

