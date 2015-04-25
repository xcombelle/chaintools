#!myfunction(param1="a",param2="b")|prog {param1} "param2"
import fileinput
import sys


def cat(*names):
    def _cat(input):
        if names:
            input = fileinput.input(*names)
        else:
            input = sys.stdin
        for elt in input:
            yield elt.rstrip("\n")
               
    return _cat

def output(end=None):
    def _output(input):
        for line in input:
            print(line,end=end)
    return _output

def split(separator=None):
    def _split(input):
        yield from (line.split(separator) for line in input)
    return _split

def sort(key=None,reverse=False):
    def _sort(input):
        yield from sorted(input,key=key,reverse=reverse)
    return _sort

def join(separator=""):
    def _join(input):
        yield from (separator.join(line) for line in input)
    return _join


def chain_generators(*generators):
    input = None
    for generator in generators:
        input = generator(input)
    return generator


def filter(func):
    def _filter(input):
        yield from (elt for elt in input if func(elt)) 
    return _filter
    
def map(func):
    def _map(input):
        yield from (func(elt) for elt in input)
    return _map

def take(n):
    def _take(input):
        for i,elt in enumerate(input):
            yield elt 
            if i == n:
                break
    return _take


if __name__ == "__main__":
    if sys.argv[1] == "1":
        chain_generators(cat(sys.argv[2:]),
                         split(","),
                         sort(key=lambda k:int(k[1]),reverse=True),
                         join("\t"),
                         output())

    elif sys.argv[1] == "2":
        chain_generators(cat(),
                         filter(lambda s: s and s[0] != '#'),
                         map(float),
                         sort(),
                         take(10),
                         output())
                     
#endnew