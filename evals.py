#! /usr/bin/python
# -*- coding:utf-8 -*-

from Kuin import *

def whtype(_str):
    _type = u"None"
    if _str.isdigit():
        _type = u"int"
    elif _str in [u"true", u"false"]:
        _type = u"bool"
    elif _str[0] == '"' and _str[-1] == '"':
        _type = u"char"
    return _type

class Eval(object):
    def __init__(self):
        self.ops = [x[0] for x in Operators]
        self.functions = []
        self.values = []
        self.elements = []
        self.index = -1
        self.excompile = []

    def setfile(self, _filename):
        self.fname = _filename.split("/")[-1].split(".")[0]
        self.current_fname = self.fname

    def newlex(self, token):
        if self.elements != []:
            for i in range(len(self.elements)):
                if token[3] == self.elements[i][4] and token[2] == self.elements[i][3]:
                        print u"Error: E3298 already declared\n", token

        self.elements.append([self.current_fname]+token)
        self.index += 1
        if token[0] == u"func":
            self.functions.append([token[3],self.index])
        elif token[0] == u"var":
            self.values.append([token[3],self.index])

    def replex(self, _index, _value):
        self.elements[self.index][_index] = _value

    def execute(self, _token, depth):
        return self.rpn2py(self.txt2rpn(_token, depth))

    def findval(self, _token, depth):
        isFound = False
        _depth = depth.split("_")
        for i in range(len(self.values)):
            if _token == self.values[i][0]:
                d = self.elements[self.values[i][1]][3].split("_")
                if (d[0] < _depth[0] or (d[0] == _depth[0] and d[1] == _depth[1])):
                    isFound = True
        return isFound

    def rpn2py(self, _token):
        _out = []
        index = -1
        right = 0
        offset = 0

        arg = []
        for i in range(len(_token)):
            if _token[i][0] in self.ops:
                _idx = self.ops.index(_token[i][0])

                # ()のある処理
                if len(arg) < len(_token[i])-2:
                    print u"Error: E00?? 演算子の対応が取れません\n", arg
                else:
                    _type = arg[0]
                    for j in arg:
                        if _type != j:
                            print u"Error: E0??? 演算子の型が合いません\n", arg

                    arg[-Operators[_idx][4]:] = [arg[-1]]
                    
                if Operators[_idx][4]==1:
                    _out[index-1:] = [Operators[_idx][3]+_out[index-1]]
                elif Operators[_idx][4]==2:
                    _out[index-1:] = [u"("+_out[index-1]+Operators[_idx][3]+_out[index]+u")"]

                index -= Operators[_idx][4]
            elif _token[i][0].split(u".")[-1] in [x[1] for x in self.excompile]:
                _out.append(_token[i][0])
                arg.append(u"int")
            elif _token[i][0].split(u"(")[0] in [x[0] for x in self.functions]:
                _out.append(_token[i][0])
                arg.append(_token[i][-1])
            else:
                _out.append(_token[i][0])
                arg.append(_token[i][1])
            index += 1

        if len(_out)!=1:
            for i in range(index):
                _out[0] = _out[i+1]+u"("+_out[0]+u")"

        return [_out[0], arg[0]]

    def txt2rpn(self, _token, depth):
        _prior = MAX_OPRI
        _out = []
        _stack = [[]]
        _braket = 0
        mode = ""
        pre_braket = -1

        arg = []
        pre_arg = []
        for i in range(len(_token)):
            if _token[i] == u"": continue
            _type = whtype(_token[i])
            if mode == "type":
                if not _token[i] in Types:
                    print u"Cautoin:C00?? 定義されていない型です。\n", _token[i]
                mode = ""
#                _out[-1] = _token[i]+u"("+_out[-1]+u")"
                _out[-1] = [_token[i]+u"("+_out[-1]+u")",_token[i]]
            elif mode == "arg":
                if _token[i] == u"(":
                    mode = "args"
                else: print u"Error: E3298 Unexpected Error!"
            elif _token[i] == u"": continue
            elif self.findval(_token[i], depth):
                _this = self.elements[self.values[[x[0] for x in self.values].index(_token[i])][1]]
                _out.append([_token[i], _this[2]])
            elif _token[i] == u"(":
                _braket += 1
                _stack.append([])
            elif _token[i] == u")" and _braket != pre_braket:
                _braket -= 1
                _out += _stack[-1][::-1]
                _stack.pop()
            elif mode == "args":
                if _token[i] == u")" and _braket == pre_braket:
                    _arg = [[]]
                    for i in arg:
                        if i == u",": _arg.append([])
                        else: _arg[-1].append(i)

                    if pre_arg == [[]]:
                        if _arg != [[]]:
                            print u"Error: E3232 too many or less arguments\n", _arg
                    elif _arg == [[]]:
                        if pre_arg != [[]]:
                            print u"Error: E3232 too many or less arguments\n", _arg
                    elif len(pre_arg) != len(_arg):
                        print u"Error: E3232 too many or less arguments\n", _arg

                    if _this[5] != pre_arg:
                        print u"Error: E2334 not proper type\n", _arg
                    else:
                        if _this[5] == [[]]:
                            _stack[-1][-1][0] += u"()"
                        else:
                            _stack[-1][-1][0] += u"("+u",".join([x[0] for x in _this[5]])+u")"
                    mode = ""
                    pre_braket = -1
                else:
                    arg.append(_token[i])
            elif _token[i] in self.ops:
                idx = Operators[self.ops.index(_token[i])]
                if idx[4] == 1:
                    _stack[-1].append([_token[i],u"any",u"any"])
                elif idx[4] == 2:
                    prior = idx[1]
                    if prior < _prior+_braket*MAX_OPRI:
                       _stack[-1].append([_token[i],u"any",u"any",u"any"])
                    else:
                        _out += _stack[-1][::-1]
                        _stack[-1] = [[_token[i],u"any",u"any",u"any"]]
                    _prior = prior
            elif u"@" in _token[i]:
                name = _token[i].split(u"@")
                self.excompile.append(name)
                if name[1] in [x[0] for x in self.functions]:
                    _this = self.elements[[x[0] for x in self.functions].index(name[1])]
                    if _this[5] == [[]]:
                        _stack[-1].append([name[1]]+[_this[2]])
                    else:
                        _stack[-1].append([name[1]]+[x[1] for x in _this[5]]+[_this[2]])
                    mode = "arg"
                    pre_braket = _braket
                    pre_arg = _this[5]
                else:
                    _stack.append([[name[0]+u"."+name[1]]])
            elif _token[i] == u":":
                mode = "type"
            elif _token[i] == u"import":
                _out.append(" ".join(_token[i:]))
            elif _type != u"None":
                if _type == u"bool":
                    _token[i] = _token[i][0].upper()+_token[i][1:]
#                _out.append(_token[i])
                _out.append([_token[i], _type])
            else:
                print u"SyntaxError:不明なトークンです\n",_token[i],_token
        if _stack == [[]]:
            pass
        else: _out += _stack[-1][::-1]

        return _out

