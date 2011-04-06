# -*- coding: utf8 -*-

import os
import unittest
from arrangemusic_tools import processing, config
from mock import *




class TestConfig(unittest.TestCase):
			
	def test_config_arg_parse(self):
		options = config.Configuration()
		options.read('test.cfg')
				
		self.assertEqual(options.pattern, 'default')
		self.assertFalse(options.dryrun)
		self.assertFalse(options.move)
				
		parser = config.CmdlineParser()
		argv = ["-nm","-p","multi", "file"]
		files = parser.parse(argv)
		self.assertEqual(options.pattern, 'multi')
		self.assertTrue(options.dryrun)
		self.assertTrue(options.move)
		
		self.assertEqual(files, ['file'])
	
	def test_config_singleton(self):
		self.assertTrue(id(config.Configuration()) == id(config.Configuration()))
	

		
class TestArrangeMusic(unittest.TestCase):
	
	def setUp(self):
		self.options = config.Configuration()
		self.options.read('test.cfg')
		self.tagm = TagPyFileRefMock("testfile.mp3")
		self.tagm.settag(artist="test", title="file", track=0, year=2001, genre="", album="Test Case")
	
	def test_tagInfo(self):
		tagm = self.tagm
				
		tag = processing.TagInfo(tagm)
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
		tag = processing.TagInfo(tagm)
		self.assertEqual(tag.year, '')
		
		tagm.filename = "mh.fac"
		tagm.settag(title="whatever you want", track=5, artist="Test")
		tag = processing.TagInfo(tagm)
		path = tag.makePath()
		self.assertEqual(path, "T/Test//05.Whatever_You_Want.")
		
		tagm.filename = u"höher.mp3"
		tagm.settag(title=u"Höher…", track=0, artist=u"Pilot", album=u"Über den Wolken")
		tag = processing.TagInfo(tagm)
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
		tag = processing.TagInfo(tagm)
		argv = ["-vt", "/tmp", "testfile.mp3"]
		options = config.Configuration()
		parser  = config.CmdlineParser()
		files   = parser.parse(argv)
		self.assertTrue(options.verbose)
		self.assertEqual(options.target_dir, "/tmp")
		self.assertEqual(files, ["testfile.mp3"])
		
		path = tag.makePath()
		self.assertEqual(path, "T/Test/2001-Test_Case/File.mp3")
	
	
	def test_run(self):
		print
		argv = ['-n', './']
		gen = TagGenerator(artist='The Wall', album='Bricks', title=u'Who’s number {track}?')
		processing.run(argv, gen.next)
		
		
		