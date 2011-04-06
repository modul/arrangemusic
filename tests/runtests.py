#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest, doctest
import tests
from arrangemusic_tools import config, processing, singleton

if __name__ == '__main__':
	print "TESTING HELP"
	config.CmdlineParser().help()
	print
	
	print "RUNNING DOCTESTS"
	print "in processing"
	suite = doctest.DocTestSuite(processing)
	unittest.TextTestRunner(verbosity=2).run(suite)
	
	print "RUNNING TESTCASES"
	suite = unittest.TestLoader().loadTestsFromModule(tests)
	unittest.TextTestRunner(verbosity=2).run(suite)
