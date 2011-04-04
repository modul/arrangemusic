# -*- coding: utf8 -*-

import unittest, doctest
import arrangemusic
import os
from config import Configuration


class TagMock(object):
	def __init__(self, filename):
		self.artist = ""
		self.album  = ""
		self.genre  = ""
		self.track  = 0
		self.title  = ""
		self.year   = 0
		self.filename = filename
	
		

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
	

		
class TestProcessTag(unittest.TestCase):
	
	def setUp(self):
		self.tag = TagMock("testfile.mp3")
		self.tag.artist = "test"
		self.tag.title  = "file"
		self.tag.track  = 0
		self.tag.year   = 2001
		self.tag.genre  = ""
		self.tag.album  =  "Test Case"
	
	def test_tagInfo(self):
		tag = arrangemusic.TagInfo(self.tag)
		self.assertEqual(tag.artist, 'Test')
		self.assertEqual(tag.title, 'File')
		self.assertEqual(tag.track, '')
		self.assertEqual(tag.year, 2001)
		self.assertEqual(tag.genre, 'No Genre')
		self.assertEqual(tag.album, 'Test Case')
		
	def test_fileListing(self):
		exts = ['.py']
		listing = arrangemusic.file_listing('.', exts)
		self.assertTrue('./arrangemusic.py' in listing)
		self.assertTrue('./config.py' in listing)
		self.assertTrue('./tests.py' in listing)
		self.assertFalse('./config.pyc' in listing)
	
		
		