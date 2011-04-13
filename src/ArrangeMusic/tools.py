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
from configuration import *

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
		if filename.lower().endswith(ext.lower()):
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
	""" Return a listing of files with 'extensions'. """
	results = []
	for dirpath, dirs, files in os.walk(directory):
		for f in files:
			if get_extension(f, extensions):
				results.append(os.path.join(dirpath, f))
	return results


def get_first(s, matches):
	"""
	If the first word of 's' is in 'matches' it returns a tuple with the match
	and the rest of 's'.
	
	>>> get_first("The World", ['The'])
	('The', 'World')
	>>> get_first("Hello World", ['The'])
	('', 'Hello World')
	>>> get_first("Hello", [])
	('', 'Hello')
	>>> get_first("the answer", ['The'])
	('the', 'answer')
	>>> get_first("hello", ['hello'])
	('', 'hello')
	"""
	words = s.split()
	if len(words) > 1 and words[0].lower() in (x.lower() for x in matches):
		return (words[0], ' '.join(words[1:]))
	else:
		return ('', s)

def print_overview():
	"""
	Prints options and configuration.
	"""
	options = Configuration()
	print "\033[33m"

	if len(options.cfg_files) == 0:
		print "No configuration (use -f to supply one)"
	if options.dryrun:
		print "Dry-run (just pretending, use -d to overwrite)"
	if options.interactive: 
		print "Interactive (use -I to don't get asked on each file)"
	if options.verbose:
		print "Verbose (use -q to stop spam)" 
	if options.move:
		print "Removing source files (use -c to keep them)"
	print "Using pattern '{pat}' (change with -p)".format(pat=options.pattern)
	
	print "Target directory:", options.target_dir, "(change with -t DIRECTORY)"
	print "\033[0m"
	
	if options.verbose:
		print "FILE PATTERN  :", options.newpath
		print "TRACK PATTERN :", options.trackstyle
		print "YEAR PATTERN  :", options.yearstyle
		print "ALBUM PATTERN  :", options.albumstyle
		print