# -*- coding: utf8 -*-
#
# Base class to create Singleton objects
#
# author: Remo Giermann <mo@liberejo.de>
# created: 2010/04/04
#

class Singleton(object):
	"""
	Singleton
	Implements getInstance method, needs a little trick with class definition
	to prevent calling __init__ a second time.

	>>> class MyClassSingleton(Singleton):
	...    def __init__(self, i): # only called on first instantiation, setup attributes here
	...        self.i = i
	>>> MyClass = MyClassSingleton.getInstance
	>>> a = MyClass(5)
	>>> b = MyClass(6) # second initialization has no effect
	>>> a.i == 5
	True
	>>> b.i == 5
	True
	>>> a == b
	True
	>>> c = MyClass()
	>>> c.i == 5
	True
	>>> c.i = 1000
	>>> a.i == 1000
	True
	"""
	__instance = None
	
	@classmethod
	def getInstance(cls, *args, **kwargs):
		if cls.__instance is None:
			cls.__instance = cls(*args, **kwargs)
		return cls.__instance