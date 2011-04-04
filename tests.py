# -*- coding: utf8 -*-

import unittest, doctest
import arrangemusic


class TestClean(unittest.TestCase):
	
	def setUp(self):
		self.replacements = {' ': '_', '/': '_'}
	
	def test_clean(self):
		s = "Hello World/Other People!"
		self.assertEqual(arrangemusic.clean(s, self.replacements), "Hello_World_Other_People!")



