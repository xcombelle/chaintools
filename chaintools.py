import fileinput
import sys


def cat(*file_names):
    """
    create a generator of line in file_names files (without endline)
    """
    def _cat(input):
        if file_names:
            input = fileinput.input(*file_names)
        else:
            input = sys.stdin
        for elt in input:
            yield elt.rstrip("\n")

    return _cat

def output(end=None):
    """
    create a generator which consume input and print it to stdout
    """
    def _output(input):
        for line in input:
            print(line,end=end)
    return _output

def split(separator=None):
    """
    create a generator which split the inputs on separator
    """
    def _split(input):
        yield from (line.split(separator) for line in input)
    return _split

def sort(key=None,reverse=False):
    """
    create a generator which iter on sorted input
    """
    def _sort(input):
        yield from sorted(input,key=key,reverse=reverse)
    return _sort

def join(separator=""):
    """
    create a generator which do join on each element of input iterable
    """
    def _join(input):
        yield from (separator.join(line) for line in input)
    return _join


def filter(func):
    """
    return a generator which
    filter all element where func return true
    """
    def _filter(input):
        yield from (elt for elt in input if func(elt))
    return _filter

def map(func):
    """
    create a generator which apply func to each element of input
    """
    def _map(input):
        yield from (func(elt) for elt in input)
    return _map

def take(n):
    """
    create a generator which take the first n elements
    """
    def _take(input):
        for i,elt in enumerate(input):
            yield elt
            if i == n:
                break
    return _take

def chain(*generators,input=None):
    """
    chains each generator
    """
    for generator in generators:
        input = generator(input)
    return generator


if __name__ == "__main__":
    if sys.argv[1] == "1":
        # stupid example
        chain(cat(sys.argv[2:]),
              split(","),
              sort(key=lambda k:int(k[1]),reverse=True),
              join("\t"),
              output())

    elif sys.argv[1] == "2":
        #reddit example
        #https://www.reddit.com/r/Python/comments/33qzzf/what_features_should_python_steal_from_other/cqnof0t
        chain(cat(),
              filter(lambda s: s and s[0] != '#'),
              map(float),
              sort(),
              take(10),
              output())
