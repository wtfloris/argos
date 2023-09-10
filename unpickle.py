# Use this to quickly read data files if you want to find specific changes

import pickle

file = 'data/sample-0'

with open(file, 'rb') as read:
    print(pickle.load(read))
