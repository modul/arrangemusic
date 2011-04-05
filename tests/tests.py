# -*- coding: utf8 -*-

import unittest, doctest
from arrangemusic_tools import processing, config
import os

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


class taggenerator(object):
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


class TestConfig(unittest.TestCase):
	
	def setUp(self):
		self.options = config.Configuration('test.cfg')
	
	def test_config_arg_parse(self):
		options = self.options
		argv = ["-nm","-p","multi", "file"]
		
		self.assertEqual(options.pattern, 'default')
		self.assertFalse(options.dryrun)
		self.assertFalse(options.move)
				
		files = options.parseArguments(argv)
		self.assertEqual(options.pattern, 'multi')
		self.assertTrue(options.dryrun)
		self.assertTrue(options.move)
		
		self.assertEqual(files, ['file'])
	
	#def test_config_print_help(self):
		#self.options.help()
	

		
class TestArrangeMusic(unittest.TestCase):
	
	def setUp(self):
		self.options = config.Configuration('test.cfg')
		self.tagm = TagPyFileRefMock("testfile.mp3")
		self.tagm.settag(artist="test", title="file", track=0, year=2001, genre="", album="Test Case")
	
	def test_tagInfo(self):
		tagm = self.tagm
				
		tag = processing.TagInfo(tagm, self.options)
		self.assertEqual(tag.artist, 'Test')
		self.assertEqual(tag.title, 'File')
		self.assertEqual(tag.track, '')
		self.assertEqual(tag.year, 2001)
		self.assertEqual(tag.genre, 'No Genre')
		self.assertEqual(tag.album, 'Test Case')
		self.assertEqual(tag.filename, "testfile.mp3")
		self.assertEqual(tag.extension, "mp3")
		
		path = tag.makePath()
		self.assertEqual(path, "T/Test/2001-Test_Case/File.mp3")
		
		tagm.settag(year=0)
		tag = processing.TagInfo(tagm, self.options)
		self.assertEqual(tag.year, '')
		
		tagm.filename = "mh.fac"
		tagm.settag(title="whatever you want", track=5, artist="Test")
		tag = processing.TagInfo(tagm, self.options)
		path = tag.makePath()
		self.assertEqual(path, "T/Test//05.Whatever_You_Want.")
		
		tagm.filename = u"höher.mp3"
		tagm.settag(title=u"Höher…", track=0, artist=u"Pilot", album=u"Über den Wolken")
		tag = processing.TagInfo(tagm, self.options)
		path = tag.makePath()
		self.assertEqual(path, "P/Pilot/Über_Den_Wolken/Höher….mp3")
		
	
	def test_file_listing(self):
		exts = ['.py']
		listing = processing.file_listing('.', exts)
		self.assertTrue('./runtests.py' in listing)
		self.assertTrue('./tests.py' in listing)
		self.assertFalse('./tests.pyc' in listing)


	def test_commandline_process_file(self):
		tagm = self.tagm
		tag = processing.TagInfo(tagm, self.options)
		argv = ["-vt", "/tmp", "testfile.mp3"]
		options = self.options
		files = options.parseArguments(argv)
		self.assertTrue(options.verbose)
		self.assertEqual(options.target_dir, "/tmp")
		self.assertEqual(files, ["testfile.mp3"])
		
		path = tag.makePath()
		self.assertEqual(path, "T/Test/2001-Test_Case/File.mp3")
	
	
	def test_run(self):
		print
		argv = ['-n', './']
		gen = taggenerator(artist='The Wall', album='Bricks', title=u'Who’s number {track}?')
		processing.run(argv, gen.next, 'test.cfg')
		
		
		