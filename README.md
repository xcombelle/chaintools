# Presentation

The purpose of this library is to make available unix tools like with a pythonic syntax. It presents pipeline tools

An example of use is

	chain(cat(),
          filter(lambda s: s and s[0] != '#'),
          map(float),
          sort(),
          head(n=10),
          output())

The secret for using this syntax is for one part the chain function which
chain generators and the generator which are created by the generator
factories (called also tool). Several generator factories are available see [builtins tools (generator factories)][]. It's easy to build your own generator factory (see [build your own tool (generator factory)][])

# Status

This library is still in pre-0.1 status. So it is expected to change.

The run generator factory is especially not full complete (for example only read and write in utf-8 unicode python values and only available on unix)
The documentation (only this README.md and the docstrings is still unsufisant)

A debug method would be especially usefull for debugging pipeline (I'm currently thinking about a way to capture all input output at each stage of the pipeline)

# Possible pitfalls

## as a user
The main mistake I think about is forget to add a sink at the end of the pipeline, in which case the whole pipeline is itself an iterator which does nothing

## as a tool (generator factory) builder
The pitfall I fell it in creating them was simply forget to return
the generator.
In these cases the chain function detect it and throw a ValueError.

# Why this syntax ?

The hope I have is to have all the power of unix tools in a pythonic way.

Reasons why all the generators use function notation:

* uniform notation: no wonder which needs and which not need parenthesis.
* make think that the generator does something

I believe that the generator factories have corresponding behaviour than caracteristics of unix tools like command switch (by using parameters), error code (by using exception). The only missing part is the standard error.

The main difference is that there is not a processus by tool (except when running an external program):
* there is not native parallelization of tools 
* there is no need to create a processus for each tool

A great avantage of chaintools is that the types are not limited to byte stream.
An example of this power is the join and split tools which has no equivalent (to my knowledge) in unix tools.


# build your own tool (generator factory)

a generator factory is a strange beast at the first see but it is not so
complicated

    def filter(func):
		"""
		return a generator which
		filter all element where func return true
		"""

        # note that the func is a parameter of the generator factory
        # which is used only by the generator
		
		def _filter(input):
		    # for correct use all generator have to have a single parameter
            # which is the input
            # and generate the result
			yield from (elt for elt in input if func(elt))
		return _filter


# what can I import ?

and easy import of all functionnality now available is 

	from chaintools import (
		chain,
		grep,
		run,
		cat,
		output,
		split,
		sort,
		join,
		map,
		head,
		tail,
		null,
	)

be aware that it **shadows map and filter builtins**

# builtins tools (generator factories)

the protoype of builtins generator factories are the following

	def cat(*file_names):

	def grep(pattern,flags=0):

	def output(end=None):

	def split(separator=None):

	def sort(key=None,reverse=False):

	def join(separator=""):

	def filter(func):

	def map(func):

	def head(n=10):

	def tail(n=10):

	def null()

	def chain(*generators,input=None):

	def run(command):
	#only works under unix
