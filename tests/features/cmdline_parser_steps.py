from lettuce import *
from arrangemusic_tools import configuration

def tobool(s):
	if s.lower() == 'true':
		return True
	else:
		return False


@step(u'Given I have my commandline parser object created')
def parser_created(step):
	world.parser = configuration.CmdlineParser()

@step(u'When I let it parse an empty argument list')
def parse_empty_list(step):
	world.parser.parse([])

@step(u'Then a configuration instance will hold default options')
def configuration_has_defaults(step):
	conf = configuration.Configuration()
	assert conf.interactive is False
	assert conf.pattern == "internal"
	assert conf.dryrun is True
	assert conf.verbose is False

@step(u'Given I have my commandline parser object created after changing configurration options')
def parser_after_changing_configuration_options(step):
	conf = configuration.Configuration()
	conf.interactive = True
	world.sth = True
	world.parser = configuration.CmdlineParser()

@step(u'Then the configuration should not be altered')
def configuration_should_not_be_altered(step):
	conf = configuration.Configuration()
	#world.sth = True
	assert world.sth == conf.interactive
	conf.interactive = not world.sth
	assert conf.interactive is not world.sth

@step(u'When I let it parse (-.*$)')
def parse_args(step, args):
	a = args.split()
	world.parser.parse(a)
	
#@step(u'Then I will have the options <dryrun>, <verbose>, <interactive>, <target_dir>, <move> set or unset'
@step(r'Then I will have the options (True|False), (True|False), (True|False), ([a-zA-Z./]+), (True|False) set or unset')
def options_set(step, dryrun, verbose, interactive, target_dir, move):
	conf = configuration.Configuration()
	assert conf.dryrun is tobool(dryrun), dryrun
	assert conf.verbose is tobool(verbose), verbose
	assert conf.interactive is tobool(interactive), interactive
	assert conf.move is tobool(move), move
	assert conf.target_dir == target_dir, target_dir

