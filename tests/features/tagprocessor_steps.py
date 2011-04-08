# -*- coding: utf-8 -*-                                                                                                                                         
from lettuce import *

from mock import *
from arrangemusic_tools import config, processing

@step(u'Given I have the configuration from "(.*)"')
def configuration_from_filename(step, filename):
	conf = config.Configuration()
	conf.read(filename)
    
@step(u'And I have a file "(.*)"')
def tagfile(step, filename):
	world.tag = TagPyFileRefMock(filename)
                                                                                                               
@step(u'And I have a tag like:')
def settag(step):
	tag = {}
	for h in step.hashes:
		k, v = h['key'], h['value']
		tag.update({k: v})
	world.tag.settag(**tag)

@step(u'When I load Arranger with it')
def load_arranger(step):
	world.arr = processing.Arranger(world.tag)
    
@step(u'Then it should construct "(.*)"')
def construct_the_path(step, expected):
	path = world.arr.makePath()
	if expected == "None":
		assert path == '', path
	else:
		assert path == expected, path