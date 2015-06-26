import unittest
import sys
import re

from io import StringIO


from chaintools import (
    chain,
    grep,
    sub,
    run,
    cat,
    output,
    split,
    sort,
    join,
    map,
    filter,
    head,
    tail,
    null,
)

def invalid_factory():
    def generator(input):
        yield from input
    #here should return (easy to forget)
    #return generator
    
class MyTest(unittest.TestCase):

    def assertChain(self, *generators, expected,input=[]):
        result= list(chain(*generators,input=input))
        self.assertEqual(result,expected)
        
    def test_grep(self):
        self.assertChain(
            grep(r"ab.*"),
            expected=["abc"],
            input=["abc","ABC"])

    def test_sub_string(self):
        self.assertChain(
            sub(r"/ab(.*?)/",r"hello:'\1',",count=2,flags=re.IGNORECASE),
            expected=["hello:'c',hello:'d',/abe/"],
            input=["/abc//Abd//abe/"],)

        
    def test_sub_function(self):
        def double(match):
            #print (match.groups())
            return match.group(1)*2
        self.assertChain(
            sub(r"/ab(.*?)/",double),
            expected=["ccdd"],
            input=["/abc//abd/"],)

        
    def test_run(self):
        self.assertChain(
            run("""python3 -c 'print("abc")' """),
            expected=["abc"])

    def test_invalid_factory(self):
        with self.assertRaises(ValueError):
            chain(invalid_factory())

    def test_cat_empty(self):
        oldstdin = sys.stdin
        sys.stdin = StringIO("abc")
        self.assertChain(
            cat(),
            expected=["abc"],
        )
        sys.stdin = oldstdin

    def test_cat_with_files(self):
        self.assertChain(
            cat("test_abc.txt","test_def.txt"),
            expected=["abc","def"],
        )
        
    def test_output(self):
        oldstdout = sys.stdout
        sys.stdout = StringIO()
        chain(
            output(),
            input=["abc"],
        )
        self.assertEqual(sys.stdout.getvalue(),"abc\n")
        sys.stdout = oldstdout

    def test_split(self):
        self.assertChain(
            split(","),
            expected=[["abc","def"]],
            input=["abc,def"])

    def test_sort(self):
        self.assertChain(
            sort(key=lambda s:s[0],reverse=True),
            expected=["xyz","abc","aef"],
            input=["abc","xyz","aef"])

    def test_join(self):
        self.assertChain(
            join(","),
            expected=["abc,def"],
            input=[["abc","def"]])

    def test_map(self):
        self.assertChain(
            map(int),
            expected=[1,2,3],
            input=["1","2","3"])

    def test_filter(self):
        self.assertChain(
            filter(bool),
            expected=[1,2,3],
            input=[0,1,2,3])

    def test_head(self):
        self.assertChain(
            head(n=2),
            expected=["1","2"],
            input=["1","2","3"])

    def test_tail(self):
        self.assertChain(
            tail(n=2),
            expected=["2","3"],
            input=["1","2","3"])

    def test_null(self):
        self.assertChain(
            null(),
            expected=[],
        )
        
if __name__ == '__main__':
    unittest.main()
