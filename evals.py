#! /usr/bin/python
# -*- coding:utf-8 -*-

from Kuin import *

def whtype(_str):
    _type = u"None"
    if _str.isdigit():
        _type = u"int"
    elif _str in [u"true", u"false"]:
        _type = u"bool"
    else:
        _type = u"char"
    return _type

class Eval(object):
    def __init__(self):
        self.ops = [x[0] for x in Operators]
        self.elements = []
        self.index = -1
        self.excompile = []

    def setfile(self, _filename):
        self.fname = _filename.split("/")[-1].split(".")[0]
        self.current_fname = self.fname

    def newlex(self, token):
        self.elements.append([self.current_fname]+token)
        self.index += 1

    def replex(self, _index, _value):
        self.elements[self.index][_index] = _value

    def execute(self, _token, depth):
        return self.rpn2py(self.txt2rpn(_token, depth))

    def chfunc(self, fname):
        for i in range(len(self.excompile)):
            j = self.findmember(name)
            if j == -1:
                print u"Warning:W00?? 定義されていない識別子です。\n", _token[i]
            else:
                _stack[-1]+=[name[1]]

    def findmember(self, name):
        for i in range(len(self.elements)):
            _this = self.elements[i]
            if name[0] == _this[0]:
                if name[1] == _this[4]:
                    return i
        return -1

    def rpn2py(self, _token):
        _out = []
        index = -1
        right = 0
        offset = 0

        arg = []
        for i in range(len(_token)):
#            print _out
            ###
#            if right > 0: offset = 0
#            else: offset = 0

            if _token[i][0] in self.ops:
                _idx = self.ops.index(_token[i][0])
#                if right > 0 and _token[i] != u"^":
#                    for j in range(right):
#                        if offset: _out[-2-offset:-offset] = [u"pow("+_out[-1-offset]+u","+_out[-2-offset]+u")"]
#                        else: _out[-2:] = [u"pow("+_out[-1]+u","+_out[-2]+u")"]
#                    right = 0

                # ()のある処理
                if len(arg) != Operators[_idx][4]:
                    print u"Error: E00?? 演算子の対応が取れません\n", arg
                else:
                    _type = arg[0]
                    for i in arg:
                        if _type != i:
                            print u"Error: E0??? 演算子の型が合いません\n", arg

                    arg = [arg[-1]]
#                    print arg
                    
                if Operators[_idx][4]==1:
                    _out[index-1:] = [Operators[_idx][3]+_out[index-1]]
                elif Operators[_idx][4]==2:
                        
#                    if index <= 0:
#                        print u"SyntaxError: 演算子の対応が取れません\n", _token[0]

#                    elif Operators[_idx][2] == u"right":
#                        _out[index-1:] = [_out[index-1]+Operators[_idx][3]+_out[index]]

#                    if _token[i] == u"^":
#                        right += 1
#                    else:
#                        _out[index-1:] = [u"("+_out[index-1]+Operators[_idx][3]+_out[index]+u")"]
                    _out[index-1:] = [u"("+_out[index-1]+Operators[_idx][3]+_out[index]+u")"]

                index -= Operators[_idx][4]
            elif _token[i][0].split(u".")[-1] in [x[1] for x in self.excompile]:
                pass
            else:
                _out.append(_token[i][0])
                arg.append(_token[i][1])
            index += 1

#        if right > 0:
#            for j in range(right):
#                _out[-2:] = [u"pow("+_out[-1]+u","+_out[-2]+u")"]

        if len(_out)!=1:
            for i in range(index):
                _out[0] = _out[i+1]+u"("+_out[0]+u")"

        return _out[0]

    def txt2rpn(self, _token, depth):
        _prior = MAX_OPRI
        _out = []
        _stack = [[]]
        _braket = 0
        mode = ""
        for i in range(len(_token)):
            _type = whtype(_token[i])
            if mode == "type":
                if not _token[i] in Types:
                    print u"Cautoin:C00?? 定義されていない型です。\n", _token[i]
                mode = ""
#                _out[-1] = _token[i]+u"("+_out[-1]+u")"
                _out[-1] = [_token[i]+u"("+_out[-1]+u")",_token[i]]

            elif _token[i] == u"": continue
            elif _token[i] in [x[4] for x in self.elements]:
                _this = self.elements[([x[4] for x in self.elements].index(_token[i]))]
                d = _this[3].split("_")
                _depth = depth.split("_")
                
                if not (d[0] < _depth[0] or (d[0] == _depth[0] and d[1] == _depth[1])):
                    print u"Warning:W000? 定義されていない識別子です。\n", _token[i]

#                _out.append(_token[i])
                _out.append([_token[i], _this[2]])
            elif _token[i] == u"(":
                _braket += 1
                _stack.append([])
            elif _token[i] == u")":
                _braket -= 1
                _out += _stack[-1][::-1]
                _stack.pop()
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
                if name[1] in [x[4] for x in self.elements]:
                    _stack[-1]+=[name[1]]
                else:
                    _stack.append([[name[0]+u"."+name[1]]])
            elif _token[i] == u":":
                mode = "type"
            elif _token[i] == u"import":
                _out.append(" ".join(_token[i:]))
            elif _token[i] != u"None":
                if _type == u"bool":
                    _token[i] = _token[i][0].upper()+_token[i][1:]
#                _out.append(_token[i])
                _out.append([_token[i], _type])
            else:
                print u"SyntaxError:不明なトークンです\n",_token[i]
        if _stack == [[]]:
            pass
        else: _out += _stack[-1][::-1]

        return _out

