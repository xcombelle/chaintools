import unittest
import sys

from io import StringIO


from chaintools import (
    chain,
    grep,
    run,
    cat,
    output,
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
        

if __name__ == '__main__':
    unittest.main()
