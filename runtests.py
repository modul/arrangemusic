# -*- coding: utf8 -*-

import unittest, doctest
import arrangemusic, config, tests

if __name__ == '__main__':
	print "RUNNING DOCTESTS arrangemusic"
	suite = doctest.DocTestSuite(arrangemusic)
	unittest.TextTestRunner(verbosity=2).run(suite)
	
	print "RUNNING DOCTESTS config"
	suite = doctest.DocTestSuite(config)
	unittest.TextTestRunner(verbosity=2).run(suite)
	
	print "RUNNING TESTCASES"
	suite = unittest.TestLoader().loadTestsFromModule(tests)
	unittest.TextTestRunner(verbosity=2).run(suite)
