from lettuce import *
from arrangemusic_tools import configuration

@step('I have a fresh Configuration object *')
def make_configuration(step):
	world.conf  = configuration.Configuration()

@step('I have a second Configuration object')
def make_second_configuration(step):
	world.conf2  = configuration.Configuration()

@step('both should have the same ID.')
def test_conf_and_conf2(step):
	assert id(world.conf) == id(world.conf2)

@step('"conf.(.*)" should be (.*)')
def check_configuration_option(step, opt, val):
	if val.lower() == u'true':
		val = True
	elif val.lower() == u'false':
		val = False
	assert getattr(world.conf,opt) == val, (opt, val)



