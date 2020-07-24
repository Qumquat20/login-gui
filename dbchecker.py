#!/usr/bin/python3

import pickle

def reset():
	loginfo = {'admin': 'admin'}
	pickle.dump(loginfo,open('users.p','wb'))

def check():
	db = pickle.load(open('users.p','rb'))
	for i in db:
		print(i,': ' ,db[i])

opt = input("1 to check db, 5 to reset db: ")
if opt == '1':
	check()
elif opt == '5':
	reset()