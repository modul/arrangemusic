# -*- coding: utf8 -*-
#
# Arrangemusic - config.py
# 
# Configuration file loading and commandline parsing is done here. 
# Internal defaults and options are also here. 
#
# author: Remo Giermann <mo@liberejo.de>
# created: 2010/04/04
#
 
import os
import sys
import optparse
from ConfigParser import ConfigParser

from singleton import Singleton
 
 
version = "v0.4.1"

file_extensions = ["mp3", "ogg", "flac"]
 
user_cfg = os.path.expanduser("~/.arrangemusic.cfg")
default_cfg = "/usr/local/share/arrangemusic/default.cfg"


class _Configuration(Singleton):
	"""
	Loads configuration file(s) and acts as a simple options container.
	Do not instantiate this class, use Configuration() instead.
	"""
	
	def __init__(self):
		"""
		Load configuration and setup attributes.
		"""
		self.cfg = ConfigParser()
		self.cfg_files = []
		self.read(default_cfg, user_cfg)
		
		self.verbose      = False
		self.dryrun       = True
		self.move         = False
		self.interactive  = False
		self.target_dir   = "./"
		self.pattern      = "internal"
		self.replacements = {}
		self.unk_artist   = "Unknown Artist"
		self.unk_title    = "Unknown Title"
		self.no_genre     = "No genre"
		
		self._setupPattern()

	def _setupPattern(self):
		"""
		Load rename pattern.
		"""
		pattern = self.pattern
		if pattern == "internal":
			pattern = "default"
		
		self.ignore_articles = False
		self.common_articles = ['The']
		self.trackstyle  = "{track}."
		self.albumstyle  = "{yearstyle}{album}"
		self.yearstyle   = "{year}-"
		self.newpath     = "{artist}/{albumstyle}/{trackstyle}{title}{extension}"
		self.initial_num = "first"
		
		if self.cfg.has_option(pattern, "ignore-articles"):
			self.ignore_articles = self.cfg.getboolean(pattern, "ignore-articles")
		if self.cfg.has_option(pattern, "common-articles"):
			self.common_articles = self.cfg.get(pattern, "common-articles").split(',')
		if self.cfg.has_option(pattern, "trackstyle"):
			self.trackstyle  = self.cfg.get(pattern, "trackstyle")
		if self.cfg.has_option(pattern, "albumstyle"):
			self.albumstyle  = self.cfg.get(pattern, "albumstyle")
		if self.cfg.has_option(pattern, "yearstyle"):
			self.yearstyle   = self.cfg.get(pattern, "yearstyle")
		if self.cfg.has_option(pattern, "new-path"):
			self.newpath     = self.cfg.get(pattern, "new-path")
		if self.cfg.has_option(pattern, "initial-of-number"):
			self.initial_num = self.cfg.get(pattern, "initial-of-number")
		
	def read(self, *args):
		"""
		Reads one or more additional configuration files and updates options.
		"""
		for cfgfile in args:
			if not cfgfile in self.cfg_files:
				self.cfg_files.extend(self.cfg.read(cfgfile))
		
		if len(self.cfg_files) > 0:
			if self.cfg.has_option("commandline", "verbose"):
				self.verbose = self.cfg.getboolean("commandline", "verbose")
				
			if self.cfg.has_option("commandline", "pretend"):
				self.dryrun = self.cfg.getboolean("commandline", "pretend")
				
			if self.cfg.has_option("commandline", "move"):
				self.move = self.cfg.getboolean("commandline", "move")
				
			if self.cfg.has_option("commandline", "interactive"):
				self.interactive = self.cfg.getboolean("commandline", "interactive")
				
			if self.cfg.has_option("commandline", "target"):
				self.target_dir = self.cfg.get("commandline", "target")
				
			if self.cfg.has_option("commandline", "pattern"):
				self.pattern = self.cfg.get("commandline", "pattern")
				
			if self.cfg.has_option("replacements", "replace"):
				self.replacements = eval(self.cfg.get("replacements", "replace"))
				
			if self.cfg.has_option("replacements", "unknown-artist"):
				self.unk_artist = self.cfg.get("replacements", "unknown-artist")
				
			if self.cfg.has_option("replacements", "unknown-title"):
				self.unk_title = self.cfg.get("replacements", "unknown-title")
				
			if self.cfg.has_option("replacements", "no-genre"):
				self.no_genre = self.cfg.get("replacements", "no-genre")
				
			self._setupPattern()
	
Configuration = _Configuration.getInstance


class CmdlineParser(object):
	"""
	Sets up commandline options and parses an argument list.
	"""
	
	def __init__(self):
		usage = "%prog [options] soure files/source directories ..."
		versn = "%prog "+version
		
		self.parser = optparse.OptionParser(usage=usage, version=versn)
		self._setupOptions()
	
	def _setupOptions(self):
		"""
		Setup commandline parser.
		"""
		conf = Configuration()
		
		self.parser.add_option("-f", "--configfile", help="use another configuration",
		 metavar='FILE', dest="conf", default='')
		
		actiongroup = optparse.OptionGroup(self.parser, "Actions/Interactions")
		
		actiongroup.add_option("-i", "--interactive", 
		  help="ask before doing anything", 
		  action="store_true", dest="interactive", default=conf.interactive)
		actiongroup.add_option("-I", "--non-interactive", 
		  help="don't ask",
		  action="store_false", dest="interactive", default=conf.interactive)
		actiongroup.add_option("-n", "--dry-run", 
		 help="just pretend actions",
		 action="store_true", dest="dryrun", default=conf.dryrun)
		actiongroup.add_option("-d", "--do-it", 
		 help="don't pretend actions",
		 action="store_false", dest="dryrun", default=conf.dryrun)
		actiongroup.add_option("-v", "--verbose", 
		 help="print more information",
		 action="store_true", dest="verbose", default=conf.verbose)
		actiongroup.add_option("-q", "--quiet", 
		 help="print less information",
		 action="store_false", dest="verbose", default=conf.verbose)
		
		targetgroup = optparse.OptionGroup(self.parser, "Target files")

		targetgroup.add_option("-m", "--move", 
		 help="move files (remove source files)",
		 action="store_true", dest="move", default=conf.move)
		targetgroup.add_option("-c", "--copy", 
		 help="copy files",
		 action="store_false", dest="move", default=conf.move)
		targetgroup.add_option("-t", "--target", 
		 help="move/copy files to DIRECTORY",
		 metavar="DIRECTORY", dest="target_dir", default=conf.target_dir)
		 
		patterngroup = optparse.OptionGroup(self.parser, "Patterns")
		
		patterngroup.add_option("-p", "--pattern", 
		 help="load PATTERN from configuration (other as default)",
		 metavar="PATTERN", dest="pattern", default=conf.pattern)
				
		self.parser.add_option_group(actiongroup)
		self.parser.add_option_group(targetgroup)
		self.parser.add_option_group(patterngroup)
		
		if len(conf.cfg_files) == 0:
			epilog = "No configuration file found. Default options: "
			cfg = ''
		else:
			epilog  = "Default options from {cfg} are: "

			if user_cfg in conf.cfg_files:
				cfg = user_cfg
			elif default_cfg in conf.cfg_files:
				cfg = default_cfg
			else:
				cfg = conf.cfg_files[0]
		
		epilog += "{verbose}{ask}{dry}{move}{pattern} Target directory: {target}  "
		epilog += "Rename pattern: {path}"	
		
		fmt = {'cfg': cfg,
		'verbose': conf.verbose and 'verbose, ' or '',
		'ask': conf.interactive and 'interactive, ' or '',
		'dry': conf.dryrun and '' or 'dry-run, ',
		'move': conf.move and 'move files, ' or '',
		'pattern': conf.pattern,
		'target': conf.target_dir or './',
		'path': conf.newpath
		}
		
		epilog = epilog.format(**fmt)
		self.parser.epilog = epilog
	
	def help(self):
		"""
		Print help text.
		"""
		self.parser.print_help()

	def parse(self, argv=sys.argv[1:]):
		"""
		Parse commandline, update configuration and 
		return non-option commandline arguments.
		"""
		conf = Configuration()
		(options, args) = self.parser.parse_args(argv)
		
		if options.conf:
			conf.cfg_files.extend(conf.cfg.read(options.conf))
		
		conf.verbose     = options.verbose
		conf.target_dir  = options.target_dir
		conf.interactive = options.interactive
		conf.dryrun      = options.dryrun
		conf.move        = options.move
		
		if conf.pattern != options.pattern:
			conf.pattern = options.pattern
			conf._setupPattern()
		
		return args
