#!/usr/bin/python

# Filename: helpers.py
# Author:   Aaron Karper
# Created:  2011-07-21
# Description:
# 		Provides some helper functions, namely the @assure and
#			@logging decorators and a accessor definition shortcut.
#           
import PyLogger as Logging
from PyLogger import Indent
from functools import wraps
def _(x):
	"as in @assure(_, int, float)"
	return x
class assure:
	"""Assures a certain type on function calls. Ought to raise
	an exception, if the respective argument does not satisfy its 
	precondition and return a fitting representation of the argument
	if it does. 
	
	Example:
		@assure(int)
		def f(x):
			return x+1
		
		>>> f(1)
		2
		>>> f("2")
		3
		>>> f("bla")
		ValueError: ...
		"""
	def __init__(self, *types, **keys):
		self.__types = types
		self.__keys  = keys
	def __call__(self, func):
		@wraps(func)
		def modified(*args, **key):
			return func(
					*[t(x) for t,x in zip(self.__types, args)],
					**dict([k, self.__keys[k](key[k])] for k in key))
		return modified
class Logging:
	def func_arg(self, L, D):
		return "(%s, %s)" % \
					(", ".join(map(repr, L)),
							", ".join([("%s = %s" % (k, D[k])) for k in D]))
	def __init__(self, logger = Logging.debug):
		self.__logger = logger
	def __call__(self, func):
		@wraps(func)
		def modified(*args, **key):
			with Indent(self.__logger, self.__logger.parent):
				arguments = self.func_arg(args,key)
				self.__logger("%s%s" % (func.func_name, arguments))
				return func(*args, **key)
		return modified
class loggingf(Logging):
	pass
class loggingm(Logging):
	def func_arg(self, L, D):
		return Logging.func_arg(self,L[1:], D)
class logging(loggingm):
	pass
class func_name:
	def __init__(self,name):
		self.name = name
	def __call__(self, f):
		f.func_name = self.name
		return f


def accessor(string, logger = _, type = _, immutable = False, doc = ""):
	"""Shortcut to define a property object with type checking and logging"""
	attrname = "_%s" %string
	getter = lambda self: getattr(self, attrname)
	if not immutable:
		@logging(logger)
		@assure(_,type)
		@func_name(string)
		def setter(self, val):
			setattr(self,attrname, val)
		return property(getter,setter, doc = doc)
	else:
		return property(getter, doc = doc)


