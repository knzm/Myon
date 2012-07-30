#! /usr/bin/python
# -*- coding:utf-8 -*-

from Kuin import *

class Eval(object):
    def __init__(self):
        self.ops = [x[0] for x in Operators]
        self.elements = []
        self.index = -1

    def newlex(self, *_token):
        self.elements.append(*_token)
        self.index += 1

    def replex(self, _index, _value):
        self.elements[self.index][_index] = _value

    def execute(self, _token):
        return self.rpn2py(self.txt2rpn(_token))

    def rpn2py(self, _token):
        _out = []
        index = -1
        for i in range(len(_token)):
            if _token[i] in self.ops:
                _idx = self.ops.index(_token[i])
                if Operators[_idx][4]==1:
                    _out[index-1:] = [Operators[_idx][3]+_out[index-1]]
                elif Operators[_idx][4]==2:
                    if index <= 0:
                        print u"SyntaxError: 演算子の対応が取れません\n", _token

                    _out[index-1:] = [u"("+_out[index-1]+Operators[_idx][3]+_out[index]+u")"]
#                    elif Operators[_idx][2] == u"right":
#                        _out[index-1:] = [_out[index-1]+Operators[_idx][3]+_out[index]]
                index -= Operators[_idx][4]
            else:
                _out.append(_token[i])
            index += 1
        print _out
        return _out[0]

    def txt2rpn(self, _token):
        _prior = MAX_OPRI
        _out = []
        _stack = [[]]
        _braket = 0
        for i in range(len(_token)):
            if _token[i] == u"": continue
            elif _token[i].isdigit():
                _out.append(_token[i])
                _mode = u"digit"
            elif _token[i] in [x[3] for x in self.elements]:
                _out.append(_token[i])
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
                    _stack[-1].append(_token[i])
                elif idx[4] == 2:
                    prior = idx[1]
                    if prior < _prior+_braket*MAX_OPRI:
                        _stack[-1].append(_token[i])
                    else:
                        _out += _stack[-1][::-1]
                        _stack[-1] = [_token[i]]
                    _prior = prior
            else:
                print u"SyntaxError:不明なトークンです\n",_token[i]
        if _stack == [[]]:
            pass
        else: _out += _stack[-1][::-1]

        print _out
        return _out

