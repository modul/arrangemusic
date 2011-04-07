from lettuce import *
from arrangemusic_tools import config

@step('I have a fresh Configuration object *')
def make_config_obj(step):
	world.conf  = config.Configuration()

@step('I have a second Configuration object')
def make_second_config_obj(step):
	world.conf2  = config.Configuration()

@step('both should have the same ID.')
def test_conf_and_conf2(step):
	assert id(world.conf) == id(world.conf2)

@step('"conf.(.*)" should be (.*)')
def check_config_option(step, opt, val):
	if val.lower() == u'true':
		val = True
	elif val.lower() == u'false':
		val = False
	assert getattr(world.conf,opt) == val, (opt, val)



