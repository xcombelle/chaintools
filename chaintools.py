import fileinput
import sys
import re
import shlex
import subprocess
import asyncio
import selectors
import os
import codecs
import queue

def run(command):
    """
    parse the command with help of shlex
    and create a generator which feeds the command
    with input and read output 
    
    Note: only works under unix because Pipe are not selectable under windows
    """
    command = shlex.split(command)
    
    selector = selectors.DefaultSelector()
    def _run(input):
        p=subprocess.Popen(command,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)
        
        selector.register(p.stdin, selectors.EVENT_WRITE)
        selector.register(p.stdout, selectors.EVENT_READ)
        more = memoryview(b"")
        input_offset=0
        stdout_decoder = codecs.getincrementaldecoder("utf8")()
        output = []
        while selector.get_map():
            ready = selector.select()
            for key,events in ready:
                if key.fileobj is p.stdin:
                    if input_offset==len(more):
                        try:
                            line = next(input)+"\n"
                        except StopIteration:
                            selector.unregister(key.fileobj)
                            key.fileobj.close()

                        else:
                            more= memoryview(line.encode("utf8"))
                            try:
                                input_offset = os.write(key.fd, more)

                            except BrokenPipeError :
                                selector.unregister(key.fileobj)
                                key.fileobj.close()

                    else:
                        try:
                            input_offset += os.write(key.fd, more[input_offset:])
                        except BrokenPipeError :
                            selector.unregister(key.fileobj)
                            key.fileobj.close()

                         
                elif key.fileobj == p.stdout:
                    data = os.read(key.fd,32768)
                    if not data:
                        data = stdout_decoder.decode(b"",True)
                                            
                        selector.unregister(key.fileobj)
                        key.fileobj.close()

                        if data:
                            data =  data.split("\n")
                            if data[0]:
                                output.append(data[0])
                                yield "".join(output)
                            for line in data[1:]:
                                    yield line
                    else:
                        data = stdout_decoder.decode(data)

                        while data != "":
                            try:
                                endofline = data.index("\n")
                            except ValueError:
                                output.append(data)
                                data =""
                            else:
                                output.append(data[:endofline])
                                yield "".join(output)
                                output = []
                            
                                data =data[endofline+1:]
                                            
                else:
                    raise Exception("unexpected event {}".format(key))
    return _run

def grep(pattern,flags=0):
    """
    create a generator which consume input 
    and filter the ones which match the pattern
    """
    regex = re.compile(pattern,flags)
    def _grep(input):
        yield from (line for line in input if regex.search(line))
    return _grep
        
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

def head(n=10):
    """
    create a generator which return the first n elements
    """
    def _head(input):
        for i,elt in enumerate(input):
            yield elt
            if i == n:
                break
    return _head

def tail(n=10):
    """
    create a generator which return the n last elements
    """
    
    tail_queue = queue.Queue(maxsize=n)
    def _tail(input):
        for elt in input:
            if tail_queue.full():
                tail_queue.get()
            tail_queue.put(elt)
        while not tail_queue.empty():
            yield tail_queue.get()
    return _tail

def null():
    """
    retunr an empty generator
    """
    def _null(input):
        return iter([])
    return _null

def chain(*generators,input=None):
    """
    chains each generator
    """
    for generator in generators:
        input = generator(input)
    return generator

    

if __name__ == "__main__":
    if sys.argv[1] == "run":
        chain(cat(sys.argv[2]),
              run(sys.argv[3]),
              output())
    if sys.argv[1] == "grep":
        chain(cat(sys.argv[3:]),
              grep(sys.argv[2]),
              output())
    if sys.argv[1] == "tail":
        chain(cat(sys.argv[2:]),
              tail(),
              output())
              
    elif sys.argv[1] == "1":
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
              head(10),
              output())
