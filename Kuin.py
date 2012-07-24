#! /usr/bin/python
# -*- coding:utf-8 -*-

Reserved = [
u"import" , u"func"    , u"var"    , u"const"  , \
u"alias"  , u"class"   , u"enum"   , u"end"    , \
u"if"     , u"elif"    , u"else"   , u"switch" , \
u"case"   , u"default" , u"while"  , u"skip"   , \
u"for"    , u"foreach" , u"try"    , u"catch"  , \
u"finally", u"throw"   , u"ifdef"  , u"debug"  , \
u"release", u"block"   , u"return" , u"let"    , \
u"break"  , u"continue", u"assert" , u"byte8"  , \
u"byte16" , u"byte32"  , u"byte64" , u"sbyte8" , \
u"sbyte16", u"sbyte32" , u"sbyte64", u"int"    , \
u"float"  , u"char"    , u"bool"   , u"complex", \
u"money"  , u"ratio"   , u"false"  , u"true"   , \
u"nan"    , u"inf"     , u"null"   \
]

Signs = [
u"{", u"}", u"(", u")", u",", u":" \
]

Types = [
u"int", u"char", u"bool" \
]

Operators = [
#[u"(", 15, 'left', u"("], [u")", 15, 'left', u")"], \
#[u"[", 2, 'left', u"["], [u"]", 2, 'left', u"]"], \
[u".", 2, 'left', u"."], \
[u"@new", 3, 'right', u"new"], [u"+", 3, 'right', u"+"], \
[u"-", 3, 'right', u"-"], [u"!", 3, 'right', u"not"], \
[u"@is", 4, 'left', u"is"], [u"@nis", 4, 'right', u"not is"], \
[u"@in", 4, 'left', u"in"], [u"@nin", 4, 'right', u"not in"], \
[u"$", 5, 'left'], \
[u"^", 6, 'right', 2], \
[u"*", 7, 'left', 2], [u"/", 7, 'left'], [u"%", 7, 'left'], \
[u"+", 8, 'left', 2], [u"-", 8, 'left'], \
[u"~", 9, 'left'], \
[u"<>", 10, 'left'], [u"<=", 10, 'left'], [u">=", 10, 'left'], \
[u"=", 10, 'left'], [u"<", 10, 'left'], [u">", 10, 'left'], \
[u"&", 11, 'left'], \
[u"|", 12, 'left'], \
[u"?", 13, 'left'], \
[u"::", 14, 'right'], [u":+", 14, 'right'], [u":-", 14, 'right'], \
[u":*", 14, 'right'], [u":/", 14, 'right'], [u":%", 14, 'right'], \
[u":^", 14, 'right'], [u":~", 14, 'right'] \
]

