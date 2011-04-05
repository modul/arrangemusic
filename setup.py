from distutils.core import setup

setup(name='arrangemusic',
      version='0.4',
      description='arrangemusic',
      long_description="""Create hierarchical directory/file structures of music files, based on tag information.""",
      author='Remo Giermann',
      author_email='mo@liberejo.de',
	  url='http://github.com/modul/arrangemusic',
      license='Beerware License (Rev. 42)',
      requires=['tagpy', 'ConfigParser', 'shutil'],
      platforms=['all'],

	  package_dir={'':'src'},
	  packages=['arrangemusic_tools'],
      scripts=['src/arrangemusic'],
      data_files=[('share/arrangemusic/', ['src/default.cfg'])],
      )
