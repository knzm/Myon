# -*- coding:utf-8 -*-

Reserved = [
    u"import",  u"func",     u"var",     u"const",
    u"alias",   u"class",    u"enum",    u"end",
    u"if",      u"elif",     u"else",    u"switch",
    u"case",    u"default",  u"while",   u"skip",
    u"for",     u"foreach",  u"try",     u"catch",
    u"finally", u"throw",    u"ifdef",   u"debug",
    u"release", u"block",    u"return",  u"let",
    u"break",   u"continue", u"assert",  u"byte8",
    u"byte16",  u"byte32",   u"byte64",  u"sbyte8",
    u"sbyte16", u"sbyte32",  u"sbyte64", u"int",
    u"float",   u"char",     u"bool",    u"complex",
    u"money",   u"ratio",    u"false",   u"true",
    u"nan",     u"inf",      u"null"
]

Signs = [
    u"{", u"}", u"(", u")", u",", u":"
]

Types = [
    u"int", u"char", u"bool"
]

MAX_OPRI = 15

Operators = [
    # [u"::"  , 14, 'right', u"="    , 2],
    # [u":+"  , 14, 'right', u"+="   , 2],
    # [u":-"  , 14, 'right', u"-="   , 2],
    # [u":*"  , 14, 'right', u"*="   , 2],
    # [u":/"  , 14, 'right', u"/="   , 2],
    # [u":%"  , 14, 'right', u"%"    , 2],
    # [u":^"  , 14, 'right', u"**="  , 2],
    # [u":~"  , 14, 'right', u"+="   , 2],
    # [u"?"   , 13, 'left' , u"_"    , 2],
    [u"|"   , 12, 'left' , u"or "  , 2],
    [u"&"   , 11, 'left' , u"and " , 2],
    [u"<>"  , 10, 'left' , u"!="   , 2],
    [u"<="  , 10, 'left' , u"<="   , 2],
    [u">="  , 10, 'left' , u">="   , 2],
    [u"="   , 10, 'left' , u"=="   , 2],
    [u"<"   , 10, 'left' , u"<"    , 2],
    [u">"   , 10, 'left' , u">"    , 2],
    [u"~"   , 9 , 'left' , u"+"    , 2],
    [u"+"   , 8 , 'left' , u"+"    , 2],
    [u"-"   , 8,  'left' , u"-"    , 2],
    [u"*"   , 7 , 'left' , u"*"    , 2],
    [u"/"   , 7,  'left' , u"/"    , 2],
    [u"%"   , 7 , 'left' , u"%"    , 2],
    # [u"^"   , 6 , 'right', u"pow"  , 2],
    # [u"$"   , 5 , 'left' , u"_"    , 2],
    # [u"@is" , 4 , 'left' , u"is "  , 1],
    # [u"@nis", 4,  'right', u"_"    , 1],
    # [u"@in" , 4 , 'left' , u"in "  , 1],
    # [u"@nin", 4,  'right', u"not in " , 1],
    # [u"@new", 3 , 'right', u"new  " , 1],
    # [u"+"   , 3,  'right', u"+"    , 1],
    [u"-"   , 3 , 'right', u"-"    , 1],
    [u"!"   , 3,  'right', u"not " , 1],
    # [u"("   , 2 , 'left' , u"("    , 0],
    # [u")"   , 2,  'left' , u")"    , 0],
    # [u"["   , 2 , 'left' , u"["    , 0],
    # [u"]"   , 2,  'left' , u"]"    , 0],
    [u"."   , 2 , 'left' , u"."    , 2]
]
