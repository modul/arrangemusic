#!/usr/bin/env python
# -*- coding: utf8 -*-

import unittest, doctest
import tests
from arrangemusic_tools import config, processing, tools

if __name__ == '__main__':
	print "TESTING HELP"
	config.CmdlineParser().help()
	print
	
	print "RUNNING DOCTESTS"
	suite = doctest.DocTestSuite(tools)
	unittest.TextTestRunner(verbosity=2).run(suite)
	
	print "RUNNING TESTCASES"
	suite = unittest.TestLoader().loadTestsFromModule(tests)
	unittest.TextTestRunner(verbosity=2).run(suite)
