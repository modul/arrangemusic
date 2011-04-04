 #
 # Configuration for Arrangemusic
 # 
 # Loading, commandline parsing, container class and internal defaults.
 #
 # author: Remo Giermann <mo@liberejo.de>
 # created: 2010/04/04
 #
 
import os
import optparse
from ConfigParser import ConfigParser
 
version = "v0.3.9"

file_extensions = ["mp3", "ogg", "flac"]
 
user_cfg = os.path.expanduser("~/.arrangemusic.cfg")
default_cfg = "/usr/local/share/arrangemusic/default.cfg"


class Configuration(object):
	"""
	Loads configuration file(s) and acts as a simple options container.
	
	>>> options = Configuration("default.cfg")
	>>> options.cfg_files == ["default.cfg"]
	True
	
	>>> options = Configuration()
	>>> options.newpath
	'%a/%B/%T%s.%e'
	"""
	
	def __init__(self, cfg=''):
		"""
		Load configuration and setup attributes.
		"""
		self.cfg = ConfigParser()
		read = self.cfg.read([cfg, default_cfg, user_cfg])
		
		if len(read) == 0:
			self.verbose      = False
			self.do_it        = False
			self.use_moving   = False
			self.ask_before   = False
			self.target_dir   = "./"

			self.multiartist  = False
			self.replacements = {}
			self.unk_artist   = "Unknown Artist"
			self.unk_title    = "Unknown Title"
			self.no_genre     = "No genre"
			
			self.ignore_articles = False
			self.common_articles = ['The']
			self.trackstyle  = "%t."
			self.albumstyle  = "%Y%b"
			self.yearstyle   = "%y-"
			self.newpath     = "%a/%B/%T%s.%e"
			self.initial_num = "first"
			

		else:
			self.verbose      = self.cfg.get("commandline", "verbose")
			self.do_it        = not self.cfg.getboolean("commandline", "pretend")
			self.use_moving   = self.cfg.getboolean("commandline", "move")
			self.ask_before   = self.cfg.getboolean("commandline", "interactive")
			self.target_dir   = self.cfg.get("commandline", "target")
			
			self.multiartist  = self.cfg.getboolean("commandline", "multiartist")
			self.replacements = eval(self.cfg.get("replacements", "replace"))
			self.unk_artist   = self.cfg.get("replacements", "unknown_artist")
			self.unk_title    = self.cfg.get("replacements", "unknown_title")
			self.no_genre     = self.cfg.get("replacements", "no_genre")
			
			if self.multiartist is True:
				pattern = "multiartist"
			else:
				pattern = "singleartist"
				
			self.ignore_articles = self.cfg.getboolean(pattern, "ignore_articles")
			self.common_articles = self.cfg.get(pattern, "common_articles").split(',')
			self.trackstyle  = self.cfg.get(pattern, "trackstyle")
			self.albumstyle  = self.cfg.get(pattern, "albumstyle")
			self.yearstyle   = self.cfg.get(pattern, "yearstyle")
			self.newpath     = self.cfg.get(pattern, "new_path")
			self.initial_num = self.cfg.get(pattern, "initial_of_number")
				
				
		self.cfg_files = read
		
		self.__setupOptions()

		
	def __setupOptions(self):
		"""
		Setup commandline parser.
		"""
		usage = "%prog [options] soure files/source directories ..."
		versn = "%prog "+version
		
		self.parser = optparse.OptionParser(usage=usage, version=versn)
		
		actiongroup = optparse.OptionGroup(self.parser, "Actions/Interactions")
		
		actiongroup.add_option("-i", "--interactive", 
		  help="Ask before an action is taken.", 
		  action="store_true", dest="ask_before", default=self.ask_before)
		actiongroup.add_option("-I", "--non-interactive", 
		  help="Don't ask.",
		  action="store_false", dest="ask_before", default=self.ask_before)
		actiongroup.add_option("-n", "--dry-run", 
		 help="Just pretend actions.",
		 action="store_false", dest="do_it", default=self.do_it)
		actiongroup.add_option("-d", "--do-it", 
		 help="Don't pretend actions.",
		 action="store_true", dest="do_it", default=self.do_it)
		actiongroup.add_option("-v", "--verbose", 
		 help="Print more information.",
		 action="store_true", dest="verbose", default=self.verbose)
		actiongroup.add_option("-q", "--quiet", 
		 help="Print less information.",
		 action="store_false", dest="verbose", default=self.verbose)
		
		targetgroup = optparse.OptionGroup(self.parser, "Target files")

		targetgroup.add_option("-m", "--move", 
		 help="Move files (remove source files).",
		 action="store_true", dest="use_moving", default=self.use_moving)
		targetgroup.add_option("-c", "--copy", 
		 help="Copy files.",
		 action="store_false", dest="use_moving", default=self.use_moving)
		targetgroup.add_option("-t", "--target", 
		 help="move/copy files to DIRECTORY",
		 metavar="DIRECTORY", dest="target_dir", default=self.target_dir)
		 
		patterngroup = optparse.OptionGroup(self.parser, "Patterns")
		
		patterngroup.add_option("-1", "--singleartist", 
		 help="Use single artist pattern.",
		 action="store_false", dest="multiartist", default=self.multiartist)
		patterngroup.add_option("-2", "--multiartist", 
		 help="Use multi artist pattern.",
		 action="store_true", dest="multiartist", default=self.multiartist)
		 
		self.parser.add_option_group(actiongroup)
		self.parser.add_option_group(targetgroup)
		self.parser.add_option_group(patterngroup)
		
		
		if len(self.cfg_files) == 0:
			epilog = "No configuration defaults for commandline options."
		else:
			epilog  = "Currently, the default options from {cfg} are: \n"
			epilog += "{ask} {dry} {move} {multi} {target} \n"
			epilog += "The rewrite pattern is: {pattern}\n"
			if user_cfg in self.cfg_files:
				cfg = user_cfg
			elif default_cfg in self.cfg_files:
				cfg = default_cfg
			else:
				cfg = self.cfg_files[0]
			
		
			fmt = {'cfg': cfg,
			'ask': self.ask_before and '-i' or '-I',
			'dry': self.do_it and '-d' or '-n',
			'move': self.use_moving and '-m' or '-c',
			'multi': self.multiartist and '-2' or '-1',
			'target': self.target_dir and '-t '+self.target_dir or '',
			'pattern': self.newpath
			}
			
			epilog = epilog.format(**fmt)
		
		
		self.parser.epilog = epilog
	
	
	def help(self):
		"""
		Print help text.
		"""
		self.parser.print_help()


	def parseArguments(self, argv):
		"""
		Parse commandline and update options (attributes).
		"""
		
		(options, args) = self.parser.parse_args(argv)
		
		self.target_dir  = options.target_dir
		self.ask_before  = options.ask_before
		self.do_it       = options.do_it
		self.use_moving  = options.use_moving
		self.multiartist = options.multiartist
		
		return args
	
		