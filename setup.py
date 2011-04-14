import sys
import os
import pickle
from distutils.core import setup

version = open('src/ArrangeMusic/version').readline()[:-1].split('-')[0]


# Setup script
setup(name='arrangemusic',
      version=version,
      description='Arrange Music',
      long_description="""Create hierarchical directory/file structures of music files, based on tag information.""",
      author='Remo Giermann',
      author_email='mo@liberejo.de',
	  url='http://github.com/modul/arrangemusic',
      license='Beerware License (Rev. 42)',
      requires=['tagpy', 'ConfigParser', 'shutil'],
      platforms=['all'],

	  package_dir={'':'src'},
	  package_data={'ArrangeMusic':['version']},
	  packages=['ArrangeMusic'],
      scripts=['src/arrangemusic'],
      data_files=[('share/arrangemusic/', ['src/default.cfg'])],
      )
