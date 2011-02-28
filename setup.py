from distutils.core import setup

setup(name='arrangemusic',
      version='0.3.9',
      description='arrangemusic',
      author='Remo Giermann',
      author_email='mo@liberejo.de',
      scripts=['arrangemusic'],
      data_files=[('share/arrangemusic/', ['default.cfg'])],
      license='Beerware License (Rev. 42)',
      requires=['tagpy', 'ConfigParser', 'shutil'],
      platforms=['all'],
      long_description="""Create hierarchical directory/file structers of music files, based on tag information."""
      )
