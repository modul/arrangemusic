import os
import pickle

v = pickle.load(open(os.path.join(os.path.dirname(__file__), 'version.pkl')))
__version__ = v['version']
__revision__ = v['revision']
