import os
import pickle

__versioninfo__ = pickle.load(open(os.path.join(os.path.dirname(__file__), 'version.pkl')))
