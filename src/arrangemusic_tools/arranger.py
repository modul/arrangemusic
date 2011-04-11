# -*- coding: utf8 -*-
#
# Arrangemusic - arranger.py
#
# Arranger does most of the work. 
# Processes the tag and generates a new file path.
#
# author: Remo Giermann <mo@liberejo.de>
# created: 2011/04/04
#

import sys, os, shutil
from tools import *
from configuration import *


class Arranger(object):
	"""
	Loads tag information, prepares it and moves the file.
	"""
	
	def __init__(self, tagfileref):
		self.options   = Configuration()
		self.filename  = tagfileref.file().name()
		self.extension = get_extension(self.filename, file_extensions)
		
		tag = tagfileref.tag()
		self.theartist = tag.artist or self.options.unk_artist
		self.title  = tag.title  or self.options.unk_title
		self.genre  = tag.genre  or self.options.no_genre
		self.album  = tag.album 
		self.track  = tag.track
		self.year   = tag.year
		
		self.old_artist = self.theartist
		self.old_title  = self.title
		self.old_genre  = self.genre
		self.old_album  = self.album
		self.old_track  = self.track
		self.old_year   = self.year
		
		if not self.theartist.isupper():     # leave uppercase strings as they are (e.g. ABBA)
			self.theartist = self.theartist.title()  # or convert 'bad religion' to 'Bad Religion'
		if not self.title.isupper():
			self.title  = self.title.title()
		if not self.genre.isupper():
			self.genre  = self.genre.title()
		if self.album: 
			if not self.album.isupper():
				self.album  = self.album.title()
		else: self.album = ''
		if self.track > 0:
			self.track = str(self.track).zfill(2)
		else: self.track = ''
		if self.year <= 0:
			self.year = ''
	
		self.article, self.artist = get_first(self.theartist, self.options.common_articles)
		self.first_letter = self.artist[0]
				
		if self.first_letter.isdigit():
			if self.options.initial_num == "first":
				pass
			elif self.options.initial_num == "whole":
				sp = self.artist.split()
				self.first_letter = sp[0]
			else:
				self.first_letter = c
	
	def __ask_yesno(self, question, default=False):
		"""
		Base method to ask the user a yes/no question.
		'default' marks the default answer (False means 'no').
		"""
		if default is True:
			answers = ('n', 'no') # negative answers
		else:
			answers = ('y', 'yes') # positive answers
	
		if raw_input(question).lower() not in answers:
			return default
		else:
			return not default
	
	def makePath(self):
		"""
		Perform pattern substitutions and construct a new file path.
		"""
		if self.extension == '':
			return ''
			
		theartist = replace(self.theartist, self.options.replacements)
		artist = replace(self.artist, self.options.replacements)
		title  = replace(self.title, self.options.replacements)
		genre  = replace(self.genre, self.options.replacements)
		album  = replace(self.album, self.options.replacements)
		
		if self.track:
			trackstyle = self.options.trackstyle
		else:
			trackstyle = ''
		if self.year:
			yearstyle = self.options.yearstyle
		else:
			yearstyle = ''
		if self.album:
			albumstyle = self.options.albumstyle
		else:
			albumstyle = ''

		path = self.options.newpath
		
		subst = {
			'theartist': theartist.encode('utf8'),
			'article': self.article.encode('utf8'),
			'artist': artist.encode('utf8'),
			'album':  album.encode('utf8'),
			'title':  title.encode('utf8'),
			'track':  self.track,
			'genre':  genre.encode('utf8'),
			'year' :  self.year,
			'initial'  : self.first_letter.encode('utf8'),
		}
		
		try:
			subst.update({'yearstyle' :  yearstyle.format(**subst)})
			subst.update({'albumstyle': albumstyle.format(**subst)})
			subst.update({'trackstyle': trackstyle.format(**subst)})
			
			path = path.format(**subst)
		
		except KeyError as key:
			print "Error in pattern: {0} referenced before assigned".format(key)
			return ''
		else:
			return path+'.'+self.extension
			
	def run(self):
		"""
		Copies or moves the file.
		"""
		if self.extension == '':
			print "Unacceptable file extension", self.filename
			return 
			
		options = Configuration()
		do = not self.options.dryrun
		dest = self.makePath()
		path = os.path.join(self.options.target_dir, dest)
				
		if self.options.verbose:	
			print "\nARTIST : %s -> %s" % (self.old_artist, self.theartist)
			print "ALBUM  : %s -> %s" % (self.old_album, self.album)
			print "TITLE  : %s -> %s" % (self.old_title, self.title)
			print "GENRE  : %s -> %s" % (self.old_genre, self.genre)
			print "TRACK  :", self.track
			print "TARGET :", self.options.target_dir
			print "DIR    :", os.path.dirname(path)
			print "FILE   : %s -> %s\n" % (self.filename, os.path.basename(path))
		
		if not do:
			print "Pretending:", 
		print os.path.basename(self.filename)
		print "->\033[32m TARGET/%s \033[0m" % dest
		
		if do \
		  and self.options.interactive \
		  and self.__ask_yesno("Is that OK? [Y/n] ", True) is False:
			do = False
		
		if do:
			target = os.path.dirname(path)
			if not os.path.isdir(target):
				os.makedirs(target)
			if os.path.isfile(path):
				if not self.__ask_yesno("File exists, overwrite? [N/y] ", False):
					do = False
				else:
					print "ok."
			if do:
				if self.options.move:
					shutil.move(self.filename, path)
				else:
					shutil.copy(self.filename, path)


def run(argv, mktag):
	"""
	Parses 'argv', updates configuration and prepares source files.
	To instantiate Arranger, 'mktag' is applied to the filename first.
	"""
	options = Configuration()
	parser  = CmdlineParser()
	args    = parser.parse(argv)

	if not args:
		parser.help()
		sys.exit(1)
	
	print_overview()
	print "Source(s):", args, "\n"
	
	try:
		for f in args:
			if os.path.isfile(f):
				try:
					arranger = Arranger(mktag(f))
				except ValueError:
					print "Filetype of %s not supported." % f
				else:
					arranger.run()
		
			elif os.path.isdir(f):
				args.extend(file_listing(f, file_extensions))
			else:
				print "No such file", f
				
	except KeyboardInterrupt:
		print 'Quit.'
