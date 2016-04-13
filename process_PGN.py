#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  parse_PGNs.py
#  
#  Copyright 2016 dragon <dragon@BLACKDRAGON>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import chess as chess
import chess.pgn as pgn

import random as random
import time as time

import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.externals import joblib

import pandas as pd

import matplotlib.pyplot as plt

max_game_length = 50
min_game_length = 10
max_games = 5000

PIECES = [chess.PAWN,chess.ROOK,chess.KNIGHT,chess.BISHOP,chess.QUEEN,chess.KING]

def list_to_array(L):
	a = np.zeros(64)
	for l in L:
		a[l] = 1.
	return a
	
def encode_boards_v1(board):
	#encoded_boards = []		
	#for b in boards:
	encoded_board = []
	for piece in (PIECES):
		encoded_board = np.concatenate((encoded_board,list_to_array(board.board().pieces(piece,chess.WHITE)),
			list_to_array(board.board().pieces(piece,chess.BLACK))))
			#print encoded_board
		#print b.board()
		#print encoded_board
		#encoded_boards.append(encoded_board)
	return encoded_board

def random_shuffled_boards_at_game(boards,res,ply,start_progress,end_progress = 1.0):
	late = []
	late_result = []

	late_s = []
	late_result_s = []

	'''Encoded_Boards = []
	Results  = []
	PlyCount = []
	'''
	for e,r,p in zip(boards,res,ply):
		if p > start_progress and p < end_progress:
			late.append(e)
			late_result.append(r)
			 
	#print '> 75% -->',len(late),len(late_result)
			
	### need to add shuffle

	random_order = np.random.choice(len(late_result),len(late_result),replace = False)
	#print random_order

	for r in random_order:
		late_s.append(late[r])
		late_result_s.append(late_result[r])

	#print len(late_s),len(late_result_s)
	
	return late_s,late_result_s
	
	
	
	

Encoded_Boards = []
Results  = []
PlyCount = []
Game =[]
Total_time = time.time()
start = time.time()
game_count = 0
with open ('PGN_files\games.pgn') as games:
	game = chess.pgn.read_game(games)
	while game:
		game_count +=1
		if game.headers['Site'] == '?' and not (game.headers['Result'] == '1-0' or  game.headers['Result'] == '0-1') and (int(game.headers['PlyCount'])>min_game_length and int(game.headers['PlyCount'])<max_game_length):
			game = chess.pgn.read_game(games)
			continue
		else:
			ply = 1
			node = game
			while not node.is_end():
				next_node = node.variation(0)
				node.board().san(next_node.move)
				node = next_node
				if node.board().turn:		# only positions in which white is to move next
					Encoded_Boards.append(encode_boards_v1(node))
					if game.headers['Result'] == '1-0':
						Results.append(1)
					else:
						Results.append(-1)
					# store the ply count as a % of the total game length
					PlyCount.append(ply/float(game.headers['PlyCount']))
				#print ply
				ply +=1
		if game_count > max_games :
			break
		if game_count %250 ==0:
			print 'Game -->',game_count,'Time for chunk -->',time.time()-start
			start = time.time()
		game = chess.pgn.read_game(games)
		
		
print 'Positions encoded --> ',len(Results)
print 'from',game_count,'games'
print 'Total time -->', time.time()-Total_time



boards,results=random_shuffled_boards_at_game(Encoded_Boards,Results,PlyCount,0.75)

def random_forest_test(boards,results,n_estimators = 50,test_set = 0.2):
	model = RandomForestClassifier(n_estimators = n_estimators)
	cut = int(len(results)-len(results)*test_set)
	model.fit(boards[:cut],results[:cut])
	predicts = model.predict(boards[cut:])
	proba = model.predict_proba(boards[cut:])
	real = results[cut:]
	#print 'Random Forest Test -->',metrics.accuracy_score(real,predicts)
	#print 'Random Forest Train -->',metrics.accuracy_score(results[:cut],model.predict(boards[:cut]))
	for r,p,pb in zip(real[:10],predicts[:10],proba[:10]):
		print r,p,pb
	return metrics.accuracy_score(real,predicts),metrics.accuracy_score(results[:cut],model.predict(boards[:cut])),len(boards[:cut]),len(real)



def logistic_test(boards,results, test_set = 0.2):
	model = LogisticRegression()
	cut = int(len(results)-len(results)*test_set)
	model.fit(boards[:cut],results[:cut])
	predicts = model.predict(boards[cut:])
	real = results[cut:]
	#print 'logisitic test -->',metrics.accuracy_score(real,predicts)
	#print 'logisitic train -->',metrics.accuracy_score(results[:cut],model.predict(boards[:cut]))
	
	return metrics.accuracy_score(real,predicts),metrics.accuracy_score(results[:cut],model.predict(boards[:cut])),len(boards[:cut]),len(real)

	### dummy comparisons
	dummy_uniform = DummyClassifier(strategy = 'uniform')
	dummy_uniform.fit(boards[:cut],results[:cut])

	dummy_uniform_predicts = dummy_uniform.predict(boards[cut:])
	print 'uniform dummy -->',metrics.accuracy_score(real,dummy_uniform_predicts)


	dummy_stratified = DummyClassifier(strategy = 'stratified')
	dummy_stratified.fit(boards[:cut],results[:cut])

	dummy_stratified_predicts = dummy_stratified.predict(boards[cut:])
	print 'stratified dummy -->',metrics.accuracy_score(real,dummy_stratified_predicts)

def logistic_build_save(boards,results,filename):
	model = LogisticRegression()
	#cut = int(len(results)-len(results)*.2)
	model.fit(boards,results)
	predicts = model.predict(boards)
	real = results
	#print 'logisitic test -->',metrics.accuracy_score(real,predicts)
	print 'logisitic train -->',metrics.accuracy_score(real,predicts)
	joblib.dump(model,filename)

intervals =10
result_summary = pd.DataFrame(range(intervals))
for i in range(len(result_summary)):
	result_summary.set_value(i,'Initial',0.+float(i)/intervals)
	result_summary.set_value(i,'Final',1./intervals+float(i)/intervals)
	boards,results=random_shuffled_boards_at_game(Encoded_Boards,Results,PlyCount,result_summary['Initial'][i],result_summary['Final'][i])
	test,train,test_size,train_size = logistic_test(boards,results)
	result_summary.set_value(i,'Test Accuracy',test)
	result_summary.set_value(i,'Train Accuracy',train)
	result_summary.set_value(i,'Training Examples',int(test_size))
	result_summary.set_value(i,'Test Problems',int(train_size))
	result_summary.set_value(i,'Model','Logistic Regression')
	#print result_summary.iloc[i]

plt.plot(result_summary['Initial'].values,result_summary['Train Accuracy'].values)


	

result_summary = pd.DataFrame(range(intervals))
for i in range(len(result_summary)):
	result_summary.set_value(i,'Initial',0.+float(i)/intervals)
	result_summary.set_value(i,'Final',1./intervals+float(i)/intervals)
	boards,results=random_shuffled_boards_at_game(Encoded_Boards,Results,PlyCount,result_summary['Initial'][i],result_summary['Final'][i])
	test,train,test_size,train_size = random_forest_test(boards,results)
	result_summary.set_value(i,'Test Accuracy',test)
	result_summary.set_value(i,'Train Accuracy',train)
	result_summary.set_value(i,'Training Examples',int(test_size))
	result_summary.set_value(i,'Test Problems',int(train_size))
	result_summary.set_value(i,'Model','Random Forest')
	#print result_summary.iloc[i]

plt.plot(result_summary['Initial'].values,result_summary['Train Accuracy'].values)

plt.show()
plt.savefig('plots.png')

#result_summary.to_csv('Time_Course_Results.txt',delimiter = '\t')
'''
print 'Full Range'
for _ in range(2):
	boards,results=random_shuffled_boards_at_game(Encoded_Boards,Results,PlyCount,0.0,1.)
	logistic_test(boards,results)
logistic_build_save(boards,results,'whole_logistic_white.pkl')
	
print '>90%'
for _ in range(2):
	boards,results=random_shuffled_boards_at_game(Encoded_Boards,Results,PlyCount,0.90)
	logistic_test(boards,results)

print '>75%'
for _ in range(2):
	boards,results=random_shuffled_boards_at_game(Encoded_Boards,Results,PlyCount,0.75)
	logistic_test(boards,results)

logistic_build_save(boards,results,'end_game_logistic_white.pkl')
	
print '<25%'
for _ in range(2):
	boards,results=random_shuffled_boards_at_game(Encoded_Boards,Results,PlyCount,0.0,.25)
	logistic_test(boards,results)

logistic_build_save(boards,results,'start_game_logistic_white.pkl')

'''
