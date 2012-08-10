# -*- coding:utf-8 -*-

from unittest import TestCase, main
import os

test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Kuin")


class TestParser:
    def parse(self, path):
        from main import Myon

        fname = os.path.basename(path)
        code = {}
        myon = Myon(path)
        self.parse = parse = myon.parse
        self.path = path
        myon.loadfile(path)
        parse.checkerror(True)
        code[fname] = parse.getcode(path, mode="main")
        for current_file in parse.fname:
            current_path = os.path.join(os.path.dirname(path), current_file)
            self.path = current_path
            myon.loadfile(current_path)
            code[current_file] = parse.getcode(current_path)
        parse.checkerror()
        parse.checkfunc()
        return code


sosu_expected = """\
import Kuin
def Main():
    for i in range(2,100):
        b = False
        a = 0
        for j in range(2,(i-1)):
            if ((i%j)==0):
                b = True
        if not b:
            a = (2+(3*AAA()))
def AAA():
            print "hello!"

            return 0

"""


class TestMyon(TestCase):

    def test_sosu(self):
        path = os.path.join(test_dir, "Sosu.kn")
        p = TestParser()
        code = p.parse(path)
        self.assertEquals(code["Sosu.kn"], sosu_expected)
        print code["Sosu.kn"]


if __name__ == '__main__':
    main()
