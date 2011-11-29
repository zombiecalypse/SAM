#!/usr/bin/python

# Filename: helpers.py
# Author:   Aaron Karper
# Created:  2011-11-29
import PyLogger
_ = lambda x:x
__THEADS__ = set()

version = "0.0.0"
author = "Aaron Karper <maergil@gmail.com>"

_sam_logger = PyLogger.LoggerParent()
debug = _sam_logger(PyLogger.Debug)
log = _sam_logger(PyLogger.Log)
warn = _sam_logger(PyLogger.Warn)
error = _sam_logger(PyLogger.Error)
fatal = _sam_logger(PyLogger.Fatal)


def doAsync(f,callback = _, args = tuple()):
	"Calls the function (*not* a method, closure it via lambda) `f :: argsType -> returnType` and then calls the `callback :: returnType, exception -> ignored`"
	def call(back, arg):
		try:
			val = f(*arg)
			callback(val,None)
		except Exception as e:
			try:
				error(e.message())
				callback(None,e)
			except:
				error("Callback failed")
	def callback_(thread, x):
		callback(x)
		__THREADS__.remove(thread)
	t = Thread(call, args=(callback_,args))
	__THREADS__.add(t)
	t.start()

