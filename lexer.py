#! /usr/bin/python
# -*- coding:utf-8 -*-

from Kuin import *
import evals


class Lexer(object):
    def __init__(self):
        self.index = -1
        self.eval = evals.Eval()

        self.depth = 0
        self.blockIndex = [[0, 0]]

    def analylex(self, _token, isFunc=False):
        if _token[3] == u"func":
            if isFunc:
                mode, arg, index = "(", [[]], 0
                isEnd = False
                _type = u"void"
                for i in range(len(_token)):
                    if mode == "(":
                        if _token[i] == u"(":
                            mode = "arg"
                    elif mode == "arg":
                        if _token[i] == u",":
                            arg.append([])
                            index += 1
                        elif _token[i] == u")":
                            mode = ":"
                            isEnd = True
                        elif _token[i].isalnum():
                            arg[index] += [_token[i], u"void"]
                            mode = ":"
                        else:
                            print u"Error: E3232 Unexpected Error"
                    elif mode == ":":
                        if _token[i] == u":":
                            mode = "type"
                        else:
                            print u"Error: E1121 ':'が来るべきところに来ていません。\n"
                    elif mode == "type":
                        if _token[i] in Types:
                            if isEnd:
                                _type = _token[i]
                                break
                            else:
                                mode = "arg"
                                arg[index][1] = _token[i]
                        else:
                            print u"Error: E1010 存在しない型です\n", _token[i]
                    else:
                        print u"Error: EEEE Unexpected Error"

                _token[5] = arg
                self.eval.newlex([u"func", _type, _token[0], _token[4], _token[5]])
            else:
                _token[3] = u"def"

                arg = ""
                if _token[5] != [[]]:
                    arg = u",".join([x[0] for x in _token[5]])
                _token[3] += u" " + _token[4] + u"(" + arg + u"):"

        elif _token[3] == u"for":
            self.eval.newlex([u"var", u"int", _token[0], _token[4]])

            mode, param, index = "(", [[]], 0
            for i in range(len(_token)):
                if mode == "(":
                    if _token[i] == u"(":
                        mode = "param"
                elif mode == "param":
                    if _token[i] == u",":
                        param.append([])
                        index += 1
                    elif _token[i] == u")":
                        mode = u")"
                    else:
                        param[index].append(_token[i])
                elif mode == ")":
                    if len(param) in [2, 3]:
                        break
                    else:
                        print u"SyntaxError: for()の中のパラメータの数がおかしいです><"

            _token[3] += u" " + _token[4] + u" in range(" + u",".join([y[0] for y in [self.eval.execute(x, _token[0]) for x in param]]) + u"):"
            _token[5:] = ""

        elif _token[3] == u"if":
            mode, param = "(", [u""]
            for i in range(len(_token)):
                if mode == "(":
                    if _token[i] == u"(":
                        mode = "param"
                elif mode == "param":
                    if _token[i] == u")":
                        mode = u")"
                    else:
                        param.append(_token[i])
                elif mode == ")":
                    if len(param) in [2, 3]:
                        break
                    else:
                        print u"SyntaxError: for()の中のパラメータの数がおかしいです><"

            _token[3] += u" " + self.eval.execute(param, _token[0])[0] + u":"

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
                    if _token[i] == u":":
                        mode = "type"
                    else:
                        print u"SyntaxError: :による変数の宣言が不正です><\n" + str(_token[i])
                elif mode == "type":
                    if _token[i] in Types:
                        self.eval.replex(2, _token[i])
                        mode = "::"
                    else:
                        print u"SytaxError: 存在しない型です><\n" + _token[i]
                elif mode == "::":
                    if _token[i] == u"::":
                        mode = "attr"
                    else:
                        print u"SyntaxError: ::による変数の代入が不正です><\n" + str(_token[i])
                elif mode == "attr":
                    self.eval.replex(5, _token[i])
                else:
                    print u"不明なえらー\n" + str(_token[i])

            if not mode in ["type", "attr", "::"]:
                print u"SyntaxError: varの宣言が不正です><\n" + _token[i]

            if mode == "attr":
                _this = self.eval.elements[self.index]

                _var = self.eval.execute(_this[4], _token[0])
                _val = self.eval.execute(_this[5:], _token[0])
                if _var[1] != _val[1]:
                    print u"Error: E2323 type error!\n", _var[0], _val[0]
                else:
                    _token[3] = _var[0] + u" = " + _val[0]

        elif _token[3] == u"do":
            mode = "do"
            _index = 0
            for i in range(len(_token)):
                if mode == "do":
                    if _token[i] == u"do":
                        mode = "name"
                elif mode == "name":
                    if _token[i] == "::":
                        mode = "::"
                elif mode == "::":
                    pass
                else:
                    # print u"SyntaxError: ::による変数の代入が不正です><\n" + str(_token[i])
                    print u"不明なえらー\n" + mode

            if not mode in ["name", "::"]:
                print u"SyntaxError: varの宣言が不正です><\n", mode

            if mode == "name":
                _token[3] = self.eval.execute(_token[4:], _token[0])[0]

            if mode == "::":
                _var = self.eval.execute(_token[4], _token[0])
                _val = self.eval.execute(_token[6:], _token[0])
                if _var[1] != _val[1]:
                    print u"Error: E2323 type error!\n", _var[0], _val[0]
                else:
                    _token[3] = _var[0] + u" = " + _val[0]

        elif _token[3] == u"__python__":
            _token[3] = "".join(_token[4:])

        elif _token[3] == u"import":
            _token[3] = " ".join(_token[3:])

        elif _token[3] == u"return":
            _arg = self.eval.execute(_token[4:], _token[0])
            if _token[2] != _arg[1]:
                print u"Error: E32404 Type Error!", _token, _arg
            else:
                _token[3] += u" " + _arg[0]
        else:
            print u"WARNING W0???:定義されていない識別子です。\n", _token[3]

        return _token
