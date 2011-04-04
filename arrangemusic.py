

class TagInfo(object):
	"""
	Loads tag information and prepares it.
	"""
	
	def __init__(self, filename):
		self.filename = filename
		try:
			tag = tagpy.FileRef(filename).tag()
		except ValueError:
			return False
		
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
			title  = title.title()
    
		if not self.genre.isupper():
			self.genre  = self.genre.title()
    
		if self.album: # album has not to be set
			if not self.album.isupper():
				self.album  = self.album.title()
		else: 
			self.album = ''
		
		if self.track:
			self.track = str(self.track).zfill(2)
		
		
		return True



def clean(s, replacements):
	"""
	Removes all 'kill'-characters and replaces them
	"""
	for key, value in replacements.items():
		s  = s.replace(key, value)
	return s 


def process_file(source, tag, replacements):
	
	tag.artist = clean(tag.artist, replacements)
	tag.album = clean(tag.artist, replacements)
	tag. = clean(tag.artist, replacements)