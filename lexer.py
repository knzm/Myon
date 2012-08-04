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
    
    def analylex(self, _token):
        if _token[3] == u"func":
            _token[3] = u"def"

            _out = []
            for i in _token[5:]:
                if i != u":" and i not in Types:
                    _out.append(i)

            _token[3] += u" "+_token[4]+u"".join(_out)+u":"

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
                    elif _token[i] == u")": mode = u")"
                    else:
                        param[index].append(_token[i])
                elif mode == ")":
                    if len(param) in [2, 3]: break
                    else: print u"SyntaxError: for()の中のパラメータの数がおかしいです><"

            _token[3] += u" "+_token[4] + u" in range("+str(", ".join([self.eval.execute(x, _token[0]) for x in param]))+u"):"
            _token[5:] = ""

        elif _token[3] == u"if":
            mode, param = "(", [u""]
            for i in range(len(_token)):
                if mode == "(":
                    if _token[i] == u"(":
                        mode = "param"
                elif mode == "param":
                    if _token[i] == u")": mode = u")"
                    else:
                        param.append(_token[i])
                elif mode == ")":
                    if len(param) in [2, 3]: break
                    else: print u"SyntaxError: for()の中のパラメータの数がおかしいです><"

            _token[3] += u" "+self.eval.execute(param, _token[0])+u":"

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
                        self.eval.replex(2, _token[i])
                        mode = "::"
                    else:
                        print u"SytaxError: 存在しない型です><\n"+_token[i]
                elif mode == "::":
                    if _token[i] == u"::": mode = "attr"
                    else: print u"SyntaxError: ::による変数の代入が不正です><\n"+str(_token[i])
                elif mode == "attr":
                    self.eval.replex(5, _token[i])
                else: print u"不明なえらー\n"+str(_token[i])

            if not mode in ["type", "attr"]:
                print u"SyntaxError: varの宣言が不正です><\n"+_token[i]

            if mode == "attr":
                _this = self.eval.elements[self.index]
                _token[3] = self.eval.execute([_this[4]], _token[0])+u" = "+_this[2]+u"("+self.eval.execute([_this[5]], _token[0])+")"

        elif _token[3] == u"do":
            mode = "do"
            _index = 0
            for i in range(len(_token)):
                if mode == "do":
                    if _token[i] == u"do": mode = "name"
                elif mode == "name":
                    if _token[i] == "::": mode = "::"
                elif mode == "::":
                    pass
#                    else: print u"SyntaxError: ::による変数の代入が不正です><\n"+str(_token[i])
                else: print u"不明なえらー\n"+mode

            if not mode in ["name", "::"]:
                print u"SyntaxError: varの宣言が不正です><\n",mode

            if mode == "name":
                _token[3] = self.eval.execute(_token[4:], _token[0])

            if mode == "::":
                _token[3] = self.eval.execute(_token[4], _token[0])+u" = "+self.eval.execute(_token[6:], _token[0])

        elif _token[3] == u"__python__":
            _token[3] = "".join(_token[4:])

        elif _token[3] == u"import":
            _token[3] = " ".join(_token[3:])

        else:
            print u"WARNING W0???:定義されていない識別子です。\n",_token[3]

        return _token

