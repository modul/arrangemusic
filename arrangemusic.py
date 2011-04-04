import os
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
    
		if self.album: # album has not to be set
			if not self.album.isupper():
				self.album  = self.album.title()
		else: 
			self.album = ''
		
		if self.track > 0:
			self.track = str(self.track).zfill(2)
		else:
			self.track = ''
			
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

		
		fmt = {
			'artist': artist.encode('utf8'),
			'album':  album.encode('utf8'),
			'title':  title.encode('utf8'),
			'track':  self.track,
			'genre':  genre.encode('utf8'),
			'year' :  self.year,
			'initial'  : self.first_letter.encode('utf8'),
			'extension': '.'+self.extension
		}
		
		fmt.update({'yearstyle' :  yearstyle.format(**fmt)})
		fmt.update({'trackstyle': trackstyle.format(**fmt)})	
		fmt.update({'albumstyle': albumstyle.format(**fmt)})
		
		path = self.options.newpath.format(**fmt)

		return path
		
		
	def print_changes(self):
		"""
		Print information about patterns and path rewriting.
		"""
		options = self.options
		target  = self.makePath()
		
		if options.verbose:	
			print "FILE:", self.filename, "\n"
			print "FILE PATTERN  :", options.newpath
			print "TRACK PATTERN :", options.trackstyle
			print "YEAR PATTERN  :", options.yearstyle
			print "ALBUM PATTERN  :", options.albumstyle
			print
			print "ARTIST : %s -> %s" % (self.old_artist, self.artist)
			print "ALBUM  : %s -> %s" % (self.old_album, self.album)
			print "TITLE  : %s -> %s" % (self.old_title, self.title)
			print "GENRE  : %s -> %s" % (self.old_genre, self.genre)
			print "TRACK  :", self.track
			print "TARGET :", options.target_dir
			print "DIR    :", os.path.dirname(target)
			print "FILE   : %s \n" % (os.path.basename(target))
		
		

def get_first(s, matches):
	"""
	If the first word of 's' is in 'matches' it returns a tuple with that match
	and the rest of 's'.
	
	>>> get_first("The World", ['The'])
	('The', 'World')
	>>> get_first("Hello World", ['The'])
	('', 'Hello World')
	>>> get_first("Hello", ['The'])
	('', 'Hello')
	>>> get_first("Hello World", [])
	('', 'Hello World')
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
	
	>>> exts = ['py']
	>>> listing = file_listing('.', exts)
	>>> "./arrangemusic.py" in listing
	True
	"""
	results = []
	for dirpath, dirs, files in os.walk(directory):
		for f in files:
			if get_extension(f, extensions):
				results.append(os.path.join(dirpath, f))
	return results





def run(source, target):
	print os.path.basename(source.filename), "->\033[32m", target, "\033[0m"