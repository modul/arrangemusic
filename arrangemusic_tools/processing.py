# -*- coding: utf8 -*-
#
# Arrangemusic - processing.py
#
# Everything that’s needed to process tags and files is here.
# Pattern substitution, path rewriting, file moving, file locating, tag loading etc.
#
# author: Remo Giermann <mo@liberejo.de>
# created: 2011/04/04
#



import sys, os, shutil
import config


class TagInfo(object):
	"""
	Loads tag information and prepares and processes it.
	"""
	
	def __init__(self, tagfileref, options):
		self.options   = options
		self.filename  = tagfileref.file().name()
		self.extension = get_extension(self.filename, config.file_extensions)
		
		tag = tagfileref.tag()
		self.artist = tag.artist or options.unk_artist
		self.title  = tag.title  or options.unk_title
		self.genre  = tag.genre  or options.no_genre
		self.album  = tag.album 
		self.track  = tag.track
		self.year   = tag.year
		
		self.old_artist = self.artist
		self.old_title  = self.title
		self.old_genre  = self.genre
		self.old_album  = self.album
		self.old_track  = self.track
		self.old_year   = self.year
		
		if not self.artist.isupper():     # leave uppercase strings as they are (e.g. ABBA)
			self.artist = self.artist.title()  # or convert 'bad religion' to 'Bad Religion'
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
	
		self.article, self.artist_noarticle = get_first(self.artist, options.common_articles)
		if options.ignore_articles:
			self.first_letter = self.artist_noarticle[0]
		else:
			self.first_letter = self.artist[0]
		
		if self.first_letter.isdigit():
			if option.initial_num == "first":
				pass
			elif option.initial_num == "whole":
				sp = self.artist_noarticle.split()
				self.first_letter = sp[0]
			else:
				self.first_letter = c
	
	
	def makePath(self):
		"""
		Perform pattern substitutions and construct a new file path.
		"""
	
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
			'artist': artist.encode('utf8'),
			'album':  album.encode('utf8'),
			'title':  title.encode('utf8'),
			'track':  self.track,
			'genre':  genre.encode('utf8'),
			'year' :  self.year,
			'initial'  : self.first_letter.encode('utf8'),
			'extension': '.'+self.extension
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
			return path
		

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


def process_file(source, options):
	"""
	Copies or moves a file described by 'source' (TagInfo instance).
	"""
	do = options.do_it
	
	dest = source.makePath()
	path = os.path.join(options.target_dir, dest)
			
	if options.verbose:	
		print "\nARTIST : %s -> %s" % (source.old_artist, source.artist)
		print "ALBUM  : %s -> %s" % (source.old_album, source.album)
		print "TITLE  : %s -> %s" % (source.old_title, source.title)
		print "GENRE  : %s -> %s" % (source.old_genre, source.genre)
		print "TRACK  :", source.track
		print "TARGET :", options.target_dir
		print "DIR    :", os.path.dirname(path)
		print "FILE   : %s -> %s\n" % (source.filename, os.path.basename(path))
	
	print os.path.basename(source.filename), "->\033[32m", dest, "\033[0m"
	
	if options.ask_before and do and raw_input("Is that OK? [Y/n] ") not in ('Y', 'y', ''):
		do = False
	
	if do:
		target = os.path.dirname(path)
		if not os.path.isdir(target):
			os.makedirs(target)
		if os.path.isfile(path):
			if raw_input("File exists, overwrite? [N/y] ") not in ("y", "Y"):
				print "Not overwriting."
				do = False
		if do:
			if options.use_moving:
				shutil.move(source.filename, path)
			else:
				shutil.copy(source.filename, path)
	else: 
		print "Not done."


def print_overview(options):
	"""
	Prints options and configuration.
	"""
	print "\033[33m"

	if len(options.cfg_files) == 0:
		print "No configuration (use -f to supply one)"
	if not options.do_it:
		print "Dry-run (just pretending, use -d to overwrite)"
	if options.ask_before: 
		print "Interactive (use -I to don't get asked on each file)"
	if options.verbose:
		print "Verbose (use -q to stop spam)" 
	if options.use_moving:
		print "Removing source files (use -M to keep them)"
	if options.multiartist:
		print "Multi-Artist (use -1 to use single artist pattern)"
	
	print "Target directory:", options.target_dir, "(change with -t DIRECTORY)"
	print "\033[0m"
	
	if options.verbose:
		print "FILE PATTERN  :", options.newpath
		print "TRACK PATTERN :", options.trackstyle
		print "YEAR PATTERN  :", options.yearstyle
		print "ALBUM PATTERN  :", options.albumstyle
		print


def run(argv, mktag, cfg=''):
	"""
	Parses 'argv', loads configuration and prepares source files.
	Returns a Configuration instance and a list of TagInfo instances.
	To instantiate TagInfo, 'mktag' is applied to the filename first.
	"""
	options = config.Configuration(cfg)
	args    = options.parseArguments(argv)

	if not args:
		options.help()
		sys.exit(1)
	
	print_overview(options)
	print "Source(s):", args, "\n"
	
	try:
		for f in args:
			if os.path.isfile(f):
				try:
					source = TagInfo(mktag(f), options)
				except ValueError:
					print "Filetype of %s not supported." % f
				else:
					process_file(source, options)
		
			elif os.path.isdir(f):
				args.extend(file_listing(f, config.file_extensions))
	except KeyboardInterrupt:
		print 'Quit.'
	