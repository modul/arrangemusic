# -*- coding: utf8 -*-
#
# Arrangemusic - tools.py
#
# Utility functions for file locating, character substitutions etc.
#
# author: Remo Giermann <mo@liberejo.de>
# created: 2011/04/06
#

import os

def get_extension(filename, extensions):
	"""
	Checks if 'filename' has one of 'extensions' and returns it.
	
	>>> exts = ['mp3', 'flac']
	>>> get_extension("test.mp3", exts)
	'mp3'
	>>> get_extension("test.flac", exts)
	'flac'
	>>> get_extension("test.py", exts)
	''
	"""
	for ext in extensions:
		if filename[-len(ext):].lower() == ext.lower():
			return ext
	return ''


def replace(s, replacements):
	"""
	Makes substitutions according to 'replacements' dictionary.
	
	>>> replace("Hello World!", {' ': '-'})
	'Hello-World!'
	
	"""
	for key, value in replacements.items():
		s  = s.replace(key, value)
	return s 


def file_listing(directory, extensions):
	"""
	Return a listing of files with 'extensions'.
	"""
	results = []
	for dirpath, dirs, files in os.walk(directory):
		for f in files:
			if get_extension(f, extensions):
				results.append(os.path.join(dirpath, f))
	return results


def get_first(s, matches):
	"""
	If the first word of 's' is in 'matches' it returns a tuple with that match
	and the rest of 's'.
	
	>>> get_first("The World", ['The'])
	('The', 'World')
	>>> get_first("Hello World", ['The'])
	('', 'Hello World')
	>>> get_first("Hello", [])
	('', 'Hello')
	"""
	
	sp = s.split()
	if len(sp) > 1:
		if sp[0] in matches:
			return (sp[0], ' '.join(sp[1:]))
	
	return ('', s)