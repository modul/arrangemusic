import os
import pickle
__version__ = '-'.join(open(os.path.join(os.path.dirname(__file__), 'version')).readline()[:-1].split('-')[:2])
