#
# Tools for testing
#
#

class TagPyFileRefMock(object):
	def __init__(self, filename):
		self.filename = filename
		self.tagdict = {}
	
	def settag(self, **kwargs):
		self.tagdict = kwargs
	
	def tag(self):
		return TagPyTagMock(**self.tagdict)
		
	def file(self):
		return TagPyFileMock(self.filename)
		

class TagPyTagMock(object):
	def __init__(self, **kwargs):
		self.artist = ""
		self.album  = ""
		self.genre  = ""
		self.track  = 0
		self.title  = ""
		self.year   = 0
		
		for k, v in kwargs.items():
			if self.__dict__.has_key(k):
				self.__dict__[k] = v


class TagPyFileMock(object):
	def __init__(self, filename):
		self.filename = filename
	def name(self):
		return self.filename


class TagGenerator(object):
	def __init__(self, **kwargs):
		self.artist = ''
		self.title = ''
		self.album = ''
		self.year = 0
		self.genre = ''
		self.track = 0
		
		for k, v in kwargs.items():
			if self.__dict__.has_key(k):
				self.__dict__[k] = v
		
	def next(self, filename):
		self.track += 1
		title = self.title.format(track=self.track)
		
		tag = TagPyFileRefMock(filename)
		tag.settag(artist=self.artist, title=title, album=self.album, year=self.year, genre=self.genre, track=self.track)
		return tag
