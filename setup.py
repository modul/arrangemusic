import sys
import os
import pickle
from distutils.core import setup

versionfile = 'src/ArrangeMusic/version.pkl'
if os.path.isfile(versionfile):
	versioninfo = pickle.load(open('src/ArrangeMusic/version.pkl'))
else:
	versioninfo = {'version': 0}


# Setup script
setup(name='arrangemusic',
      version=versioninfo['version'],
      description='Arrange Music',
      long_description="""Create hierarchical directory/file structures of music files, based on tag information.""",
      author='Remo Giermann',
      author_email='mo@liberejo.de',
	  url='http://github.com/modul/arrangemusic',
      license='Beerware License (Rev. 42)',
      requires=['tagpy', 'ConfigParser', 'shutil'],
      platforms=['all'],

	  package_dir={'':'src'},
	  packages=['ArrangeMusic'],
      scripts=['src/arrangemusic'],
      data_files=[('share/arrangemusic/', ['src/default.cfg'])],
      )
