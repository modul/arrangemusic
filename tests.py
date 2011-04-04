# -*- coding: utf8 -*-

import unittest, doctest
import arrangemusic
import os
from config import Configuration

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
		

class TestConfig(unittest.TestCase):
	
	def setUp(self):
		self.options = Configuration('default.cfg')
	
	def test_config_arg_parse(self):
		options = self.options
		argv = ["-nm2", "file"]
		
		self.assertTrue(options.do_it)
		self.assertFalse(options.use_moving)
		self.assertFalse(options.multiartist)
		
		options.parseArguments(argv)
		self.assertFalse(options.do_it)
		self.assertTrue(options.use_moving)
		self.assertTrue(options.multiartist)
		
		self.assertEqual(options.files, ['file'])
	
	#def test_config_print_help(self):
		#self.options.help()
	

		
class TestArrangeMusic(unittest.TestCase):
	
	def setUp(self):
		self.options = Configuration('default.cfg')
		self.tagm = TagPyFileRefMock("testfile.mp3")
		self.tagm.settag(artist="test", title="file", track=0, year=2001, genre="", album="Test Case")
	
	def test_tagInfo(self):
		tagm = self.tagm
				
		tag = arrangemusic.TagInfo(tagm)
		self.assertEqual(tag.artist, 'Test')
		self.assertEqual(tag.title, 'File')
		self.assertEqual(tag.track, '')
		self.assertEqual(tag.year, '2001')
		self.assertEqual(tag.genre, 'No Genre')
		self.assertEqual(tag.album, 'Test Case')
		self.assertEqual(tag.filename, "testfile.mp3")
		self.assertEqual(tag.extension, "mp3")
		
		tagm.settag(year=0)
		tag = arrangemusic.TagInfo(tagm)
		self.assertEqual(tag.year, '')
		
		
	def test_file_listing(self):
		exts = ['.py']
		listing = arrangemusic.file_listing('.', exts)
		self.assertTrue('./arrangemusic.py' in listing)
		self.assertTrue('./config.py' in listing)
		self.assertTrue('./tests.py' in listing)
		self.assertFalse('./config.pyc' in listing)
	
	
	def test_process_file(self):
		tagm = self.tagm
		tag = arrangemusic.TagInfo(tagm)
		path = arrangemusic.process_file(tag, self.options)
		self.assertEqual(path, "./T/Test/2001-Test_Case/File.mp3")
		
		tagm.filename = "mh.fac"
		tagm.settag(title="whatever you want", track=5, artist="Test")
		tag = arrangemusic.TagInfo(tagm)
		path = arrangemusic.process_file(tag, self.options)
		self.assertEqual(path, "./T/Test//05.Whatever_You_Want.")
		
		tagm.filename = u"höher.mp3"
		tagm.settag(title=u"Höher", track=0, artist=u"Pilot", album=u"Über den Wolken")
		tag = arrangemusic.TagInfo(tagm)
		path = arrangemusic.process_file(tag, self.options)
		self.assertEqual(path, u"./P/Pilot/Über_Den_Wolken/Höher.mp3")
		
		