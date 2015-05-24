# chaintools

It's just a **proof of concept**
which chain generator factory

available generator factories
(name should be self explained)

    def cat(*file_names):

    def grep(pattern,flags=0):

    def output(end=None):
    
    def split(separator=None):
    
    def sort(key=None,reverse=False):
    
    def join(separator=""):
    
    def filter(func):
    
    def map(func):
    
    def take(n):
    
    def chain(*generators,input=None):

example of  implementation of generator factory


    def filter(func):
        """
        return a generator which
        filter all element where func return true
        """
        def _filter(input):
            yield from (elt for elt in input if func(elt))
        return _filter


example of use

	chain(cat(),
          filter(lambda s: s and s[0] != '#'),
		  map(float),
		  sort(),
		  take(10),
		  output())
