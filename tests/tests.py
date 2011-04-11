# -*- coding: utf8 -*-

import os
import shutil

from arrangemusic_tools import arranger, configuration, tools
from mock import *

def setup():
	assert os.path.isfile('test.cfg'), "Must be run inside tests/, where test.cfg lies"	
	options = configuration.Configuration()
	options.read('test.cfg')
	assert options.target_dir == "./bla"

def make_my_tag():
	tagm = TagGenerator(artist="test", title="file", year=2001, genre="", album="Test Case").next("testfile.mp3")
	return tagm

def test_config_is_singleton():
	a = configuration.Configuration()
	b = configuration.Configuration()
	sth = a.interactive
	assert id(a) == id(b)
	b.interactive = not sth
	del a, b
	c = configuration.Configuration()
	assert c.interactive is not sth
	c.interactive = sth

def test_config_and_parser():
	options = configuration.Configuration()
	assert options.pattern == 'default-pattern', options.pattern
	assert options.dryrun is False
	assert options.move is False
	assert options.target_dir == './bla'
			
	parser = configuration.CmdlineParser()
	argv = "-nm -p multi file".split()
	files = parser.parse(argv)

	assert options.pattern == 'multi'
	assert options.dryrun is True
	assert options.move is True
	assert files == ['file']

	argv = "-c -p internal".split()
	files = parser.parse(argv)

	assert options.pattern == 'default-pattern'
	assert options.dryrun is True # options not changed by argv
	assert options.move is False  # option changed by argv   
	assert files == []

def test_config_read_from_argument():
	argv = "-f test2.cfg".split()
	parser = configuration.CmdlineParser()
	options = configuration.Configuration()
	
	assert options.interactive is False
	parser.parse(argv)
	assert 'test2.cfg' in options.cfg_files, options.cfg_files
	assert options.interactive is True
	options.interactive = False
	assert options.interactive is False

def test_arranger_taghandling():
	tagm = make_my_tag()
	tag = arranger.Arranger(tagm)
	assert tag.theartist == 'Test'
	assert tag.title == 'File'
	assert tag.track == '01'
	assert tag.year == 2001
	assert tag.genre == 'No Genre'
	assert tag.album == 'Test Case'
	assert tag.filename == 'testfile.mp3'
	assert tag.extension == 'mp3'
	
	tagm.settag(year=0)
	tag = arranger.Arranger(tagm)
	assert tag.year == ''

def test_arranger_mkpath():
	tagm = make_my_tag()
	tag = arranger.Arranger(tagm)
	path = tag.makePath()
	assert path == "T/Test/2001-Test_Case/01.File.mp3", path
	
	tagm.filename = "mh.fac"
	tagm.settag(title="whatever you want", track=5, artist="Test")
	tag = arranger.Arranger(tagm)
	path = tag.makePath()
	assert path == ""
	
	tagm.filename = u"höher.mp3"
	tagm.settag(title=u"Höher…", track=0, artist=u"Pilot", album=u"Über den Wolken")
	tag = arranger.Arranger(tagm)
	path = tag.makePath()
	assert path == "P/Pilot/Über_Den_Wolken/Höher….mp3"
	
	tagm.filename = "article test.ogg"
	tagm.settag(title="Foo bar", track=1, artist="Die sieben weltwunder", album="")
	options = configuration.Configuration()
	pat = options.newpath
	options.newpath = "{initial}/{artist},_{article}/{albumstyle}/{trackstyle}{title}"
	path = arranger.Arranger(tagm).makePath()
	assert path == "S/Sieben_Weltwunder,_Die//01.Foo_Bar.ogg", path
	options.newpath = pat

def test_file_listing():
	exts = ['.py']
	listing = tools.file_listing('.', exts)
	assert './mock.py' in listing
	assert './tests.py' in listing
	assert './tests.pyc' not in listing

def test_dryrun():
	argv = ['-n', './']
	gen = TagGenerator(artist='The Wall', album='Bricks', title=u'Who’s number {track}?')
	arranger.run(argv, gen.next)

def test_run_virtualmusic():
	argv = ['-vcd', '-t', 'virtualmusic', './']
	gen = TagGenerator(artist='The Wall', album='Bricks', title=u'Who’s number {track}?')
	arranger.run(argv, gen.next)
	assert os.path.isdir('virtualmusic/W/') is True

def test_no_wmafiles():
	listing = tools.file_listing('virtualmusic/W', ['wma'])
	assert listing == []

def teardown():
	if os.path.isdir('virtualmusic/W'):
		shutil.rmtree('virtualmusic/W/')
		assert os.path.isdir('virtualmusic/W') is False
