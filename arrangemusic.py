import os
import config


class TagInfo(object):
	"""
	Loads tag information and prepares it.
	"""
	
	def __init__(self, tagfileref):
		self.filename = tagfileref.file().name()
		self.extension = get_extension(self.filename, config.file_extensions)
		
		tag = tagfileref.tag()
		self.artist = tag.artist or "Unknown Artist"
		self.title  = tag.title or "Unknown Title"
		self.genre  = tag.genre or "No Genre"
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
			
		if self.year > 0:
			self.year = str(self.year)
		else:
			self.year = ''

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

		
def file_listing(directory, extensions):
	results = []
	for dirpath, dirs, files in os.walk(directory):
		for f in files:
			if get_extension(f, extensions):
				results.append(os.path.join(dirpath, f))
	return results


def clean(s, replacements):
	"""
	Removes all 'kill'-characters and replaces them
	
	>>> clean("Hello World!", {' ': '-'})
	'Hello-World!'
	
	"""
	for key, value in replacements.items():
		s  = s.replace(key, value)
	return s 


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
		


def process_file(source, options):
	article, artist_noart = get_first(source.artist, options.common_articles)
	
	source.artist = clean(source.artist, options.replacements)
	source.title  = clean(source.title, options.replacements)
	source.genre  = clean(source.genre, options.replacements)
	source.album  = clean(source.album, options.replacements)
    
	if source.track:
		trackstyle = options.trackstyle
	else:
		trackstyle = ''

	if source.year:
		yearstyle = options.yearstyle
	else:
		yearstyle = ''

	if source.album:
		albumstyle = options.albumstyle
	else:
		albumstyle = ''

	# Do the article ignoring if needed:
	if options.ignore_articles:
		first_letter = artist_noart[0]
	else:
		first_letter = source.artist[0]

	
	if first_letter.isdigit():
		if option.initial_num == "first":
			pass
		elif option.initial_num == "whole":
			sp = artist_noart.split()
			first_letter = sp[0]
		else:
			first_letter = c

	escapes   = ('%a','%B','%b','%s','%T','%t','%g','%Y','%y','%I','%e')   # replace the escape things with data
	replcmnts = (source.artist, albumstyle, source.album, source.title, trackstyle, source.track, source.genre, yearstyle, source.year, first_letter, source.extension)

	path = options.newpath

	for i in range(len(escapes)):
		path = path.replace(escapes[i], replcmnts[i])

	return os.path.join(options.target_dir, path)