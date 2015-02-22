#!myfunction(param1="a",param2="b")|prog {param1} "param2"
import fileinput
def cat(*names):
    def cat(input):
        yield from fileinput.input(*names)
    return cat

def output():
    def _output(input):
        for line in input:
            print(line,end="")
    return _output
def split(separator=""):
    #print("splitting",file=stderr)
    def _split(input):
        yield from (line.split(separator) for line in input)
    return _split
def sort(key=None):
    def _sort(input):
        yield from sorted(input,key=key)
    return _sort
def join(separator=""):
    def _join(input):
        yield from (separator.join(line) for line in input)
    return _join

import sys
def chain_generators(*generators):
    input = None
    for generator in generators:
        input = generator(input)
    return generator

chain_generators(cat(sys.argv[1:]),split(","),sort(key=lambda k:int(k[1])),join("\t"),output())
