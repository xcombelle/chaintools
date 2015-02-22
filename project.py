#!myfunction(param1="a",param2="b")|prog {param1} "param2"

def cat(*names,input=None,stderr=None):
    
    import fileinput
    yield from fileinput.input(*names)
    
def split(separator="",input=None,stderr=None):
    #print("splitting",file=stderr)
    yield from (line.split(separator) for line in input)

def sort(key=None,input=None,stderr=None):
    yield from sorted((line for line in input),key=key)

def join(separator="",input=None,stderr=None):
    yield from (separator.join(line) for line in input)
import sys
#!cat(sys.argv[1:])|split(",")|sort(key=lambda k:int(k[1]))|join("\t") 
def _private_pipe():
    import sys
    import functools
    _private_stderr = sys.stderr
    _private_input = []
    #print ("ici")
    def _private_make_gen(_private_input,_private_generator,*args,**kwargs):
        #print(generator.__name__)
        #print("la")
        #print("input:",input)
        #print("args:",args)
        #print("kwargs:",kwargs)
        for line in functools.partial(_private_generator,
                                      input=_private_input,
                                      stderr=_private_stderr)(*args,**kwargs):
            #print ("debug:",repr(line))
            yield line
    
    _private_input = _private_make_gen(_private_input,cat,sys.argv[1:])
    _private_input = _private_make_gen(_private_input,split,",")
    _private_input = _private_make_gen(_private_input,sort,key=lambda k:int(k[1]))
    _private_input = _private_make_gen(_private_input,join,"\t")
    for line in _private_input:
        print (line,end="")
_private_pipe()
